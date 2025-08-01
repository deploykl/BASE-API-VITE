from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils import timezone
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
import re

logger = logging.getLogger(__name__)

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    GROUP_NAME = "online_users_group"

    async def connect(self):
        await self.accept()  # Aceptar conexión primero

        # Log seguro sin mostrar el token completo
        query_string = self.scope.get("query_string", b"").decode()
        if "token=" in query_string:
            logged_token = self._secure_log_token(query_string)
            logger.info(f"Nueva conexión WebSocket (token: {logged_token})")

        # Esperar mensaje de autenticación
        self.authenticated = False

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            if data.get("type") == "authenticate" and not self.authenticated:
                await self._handle_authentication(data.get("token"))
            elif data.get("type") == "heartbeat" and self.authenticated:
                pass  # Solo mantener conexión activa
            elif self.authenticated:
                logger.warning(f"Mensaje no reconocido de usuario {self.user_id}")
        except json.JSONDecodeError:
            await self.close(code=4003)  # Código para datos inválidos

    async def _handle_authentication(self, token):
        """Maneja el proceso de autenticación"""
        if not token:
            await self.close(code=4001)
            return

        user = await self.authenticate_token(token)
        if not user:
            await self.close(code=4001)
            return

        self.user_id = user.id
        self.authenticated = True

        await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
        await self.mark_online(True)
        await self.notify_all_users()

        await self.send(
            json.dumps(
                {"type": "authentication_success", "message": "Autenticación exitosa"}
            )
        )

    def _secure_log_token(self, query_string):
        """Oculta el token en los logs"""
        match = re.search(r"token=([^&]+)", query_string)
        if match:
            token = match.group(1)
            return f"{token[:5]}...{token[-5:]}" if len(token) > 10 else "[REDACTED]"
        return "[NO_TOKEN]"

    @database_sync_to_async
    def authenticate_token(self, token):
        """Autentica el token JWT"""
        try:
            from rest_framework_simplejwt.tokens import AccessToken

            access_token = AccessToken(token)
            user_id = access_token.payload.get("user_id")
            User = get_user_model()
            return User.objects.get(id=user_id)
        except Exception as e:
            logger.error(f"Error de autenticación: {str(e)}")
            return None

    @database_sync_to_async
    def mark_online(self, is_online):
        """Actualiza el estado online del usuario"""
        User = get_user_model()
        try:
            user = User.objects.get(id=self.user_id)
            user.is_online = is_online
            user.last_login = timezone.now() if is_online else user.last_login
            user.save(update_fields=["is_online", "last_login"])
            return user
        except User.DoesNotExist:
            logger.error(f"Usuario no encontrado: {self.user_id}")
            return None

    async def notify_all_users(self):
        """Notifica a todos los usuarios la lista actualizada"""
        users = await self.get_online_users()
        await self.channel_layer.group_send(
            self.GROUP_NAME, {"type": "broadcast_users", "users": users}
        )

    @database_sync_to_async
    def get_online_users(self):
        User = get_user_model()
        users = User.objects.filter(is_online=True).values(
            "id", "username", "first_name", "last_name", "is_online"
        )

        # Manejar casos donde no hay nombre o apellido
        return [
            {
                "id": u["id"],
                "username": u["username"],
                "fullname": self._get_user_fullname(u),
                "is_online": u["is_online"],
            }
            for u in users
        ]

    def _get_user_fullname(self, user_data):
        first_name = user_data["first_name"] or ""
        last_name = user_data["last_name"] or ""

        # Obtener primer nombre y apellido si existen
        first_part = first_name.split()[0] if first_name else ""
        last_part = last_name.split()[0] if last_name else ""

        # Construir el nombre completo
        if first_part and last_part:
            return f"{first_part} {last_part}"
        elif first_part:
            return first_part
        elif last_part:
            return last_part
        else:
            return "Sin nombre"  # O puedes usar user_data['username']

    async def broadcast_users(self, event):
        """Envía la lista de usuarios a todos los clientes"""
        if self.authenticated:
            await self.send(
                text_data=json.dumps({"type": "online_users", "users": event["users"]})
            )

    async def disconnect(self, close_code):
        """Maneja la desconexión"""
        if hasattr(self, "authenticated") and self.authenticated:
            await self.mark_online(False)
            await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)
            await self.notify_all_users()
