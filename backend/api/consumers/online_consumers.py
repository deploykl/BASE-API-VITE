from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils import timezone
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
import re
from collections import defaultdict
from datetime import timedelta

logger = logging.getLogger(__name__)

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    GROUP_NAME = "online_users_group"
    active_connections = defaultdict(dict)
    HEARTBEAT_TIMEOUT = 30

    async def connect(self):
        await self.accept()
        self.user_id = None
        self.authenticated = False
        self.connection_id = f"{self.channel_name}_{timezone.now().timestamp()}"
        self.last_heartbeat = timezone.now()

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            if data.get("type") == "authenticate" and not self.authenticated:
                await self._handle_authentication(data.get("token"))
            elif data.get("type") == "heartbeat" and self.authenticated:
                await self._handle_heartbeat()
            elif self.authenticated:
                logger.warning(f"Mensaje no reconocido de usuario {self.user_id}")
        except json.JSONDecodeError:
            await self.close(code=4003)

    async def _handle_authentication(self, token):
        if not token:
            await self.close(code=4001)
            return

        auth_result = await self.authenticate_and_validate(token)
        if not auth_result or not auth_result.get("user"):
            await self.close(code=4001)
            return

        user = auth_result["user"]
        self.user_id = user.id
        self.authenticated = True
        
        self.active_connections[user.id][self.connection_id] = {
            "last_heartbeat": timezone.now(),
            "channel_name": self.channel_name
        }

        await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
        await self.mark_user_online(True)  # Cambiado de mark_online a mark_user_online
        await self.cleanup_inactive_connections()
        await self.notify_all_users()

        await self.send(json.dumps({
            "type": "authentication_success",
            "message": "Autenticación exitosa"
        }))

    async def _handle_heartbeat(self):
        if self.authenticated and self.user_id in self.active_connections:
            self.active_connections[self.user_id][self.connection_id]["last_heartbeat"] = timezone.now()
            self.last_heartbeat = timezone.now()

    @database_sync_to_async
    def authenticate_and_validate(self, token):
        try:
            from rest_framework_simplejwt.tokens import AccessToken
            from django.core.exceptions import ObjectDoesNotExist

            access_token = AccessToken(token)
            if access_token.payload.get("exp", 0) < timezone.now().timestamp():
                logger.warning("Token JWT expirado")
                return None

            user_id = access_token.payload.get("user_id")
            if not user_id:
                logger.warning("Token no contiene user_id")
                return None

            User = get_user_model()
            user = User.objects.get(id=user_id)
            
            if not user.is_active:
                logger.warning(f"Usuario inactivo intentando conectar: {user.username}")
                return None
                
            if user.username.lower() in ["admin_red", "undefined", "ghost"]:
                logger.warning(f"Intento de conexión de usuario no permitido: {user.username}")
                return None
                
            return {"user": user, "token": access_token}
        except ObjectDoesNotExist:
            logger.error("Usuario no encontrado en la base de datos")
            return None
        except Exception as e:
            logger.error(f"Error de autenticación: {str(e)}")
            return None

    @database_sync_to_async
    def mark_user_online(self, is_online):  # Método renombrado de mark_online a mark_user_online
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

    @database_sync_to_async
    def mark_user_offline(self, user_id):
        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
            if user.is_online:
                user.is_online = False
                user.save(update_fields=["is_online"])
                logger.info(f"Usuario {user.username} marcado como offline")
        except User.DoesNotExist:
            logger.error(f"Usuario no encontrado al marcar offline: {user_id}")

    async def cleanup_inactive_connections(self):
        now = timezone.now()
        users_to_mark_offline = set()

        for user_id, connections in dict(self.active_connections).items():
            active_conns = {}
            
            for conn_id, conn_data in connections.items():
                if (now - conn_data["last_heartbeat"]).total_seconds() <= self.HEARTBEAT_TIMEOUT:
                    active_conns[conn_id] = conn_data
            
            if active_conns:
                self.active_connections[user_id] = active_conns
            else:
                del self.active_connections[user_id]
                users_to_mark_offline.add(user_id)

        for user_id in users_to_mark_offline:
            await self.mark_user_offline(user_id)

    async def disconnect(self, close_code):
        if self.authenticated and self.user_id:
            if self.user_id in self.active_connections:
                if self.connection_id in self.active_connections[self.user_id]:
                    del self.active_connections[self.user_id][self.connection_id]
                
                if not self.active_connections[self.user_id]:
                    del self.active_connections[self.user_id]
                    await self.mark_user_offline(self.user_id)
            
            await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)
            await self.notify_all_users()

    @database_sync_to_async
    def get_online_users(self):
        User = get_user_model()
        online_user_ids = [user_id for user_id in self.active_connections]
        User.objects.filter(is_online=True).exclude(id__in=online_user_ids).update(is_online=False)
        
        users = User.objects.filter(
            id__in=online_user_ids,
            is_online=True
        ).values(
            "id", "username", "first_name", "last_name", "is_online"
        )
    
        return [
            {
                "id": u["id"],
                "username": u["username"],
                "fullname": self._get_user_fullname(u),
                "is_online": u["is_online"],
                "connections": len(self.active_connections.get(u["id"], {})),  # Número de conexiones
                "device_count": len(self.active_connections.get(u["id"], {}))  # Alias para claridad en frontend
            }
            for u in users
            if u["username"] and u["username"].lower() not in ["admin_red", "undefined"]
        ]

    def _get_user_fullname(self, user_data):
        first_name = user_data["first_name"] or ""
        last_name = user_data["last_name"] or ""

        first_part = first_name.split()[0] if first_name else ""
        last_part = last_name.split()[0] if last_name else ""

        if first_part and last_part:
            return f"{first_part} {last_part}"
        elif first_part:
            return first_part
        elif last_part:
            return last_part
        return user_data["username"]

    async def notify_all_users(self):
        users = await self.get_online_users()
        await self.channel_layer.group_send(
            self.GROUP_NAME, 
            {
                "type": "broadcast_users", 
                "users": users,
                "timestamp": timezone.now().isoformat()
            }
        )

    async def broadcast_users(self, event):
        if self.authenticated:
            await self.send(
                text_data=json.dumps({
                    "type": "online_users",
                    "users": event["users"],
                    "timestamp": event["timestamp"]
                })
            )

    def _secure_log_token(self, query_string):
        match = re.search(r"token=([^&]+)", query_string)
        if match:
            token = match.group(1)
            return f"{token[:5]}...{token[-5:]}" if len(token) > 10 else "[REDACTED]"
        return "[NO_TOKEN]"