from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils import timezone
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
import jwt

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Obtener token de los parámetros de consulta
        query_string = self.scope.get('query_string', b'').decode()
        token = None
        
        # Parsear el token de la query string
        for param in query_string.split('&'):
            if param.startswith('token='):
                token = param.split('=')[1]
                break
        
        if not token:
            await self.close(code=4001)
            return
            
        try:
            # Verificar token JWT
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            User = get_user_model()
            self.user = await database_sync_to_async(User.objects.get)(id=user_id)
            self.scope['user'] = self.user
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist) as e:
            await self.close(code=4001)
            return

        self.user_id = self.user.id
        self.group_name = "online_users"
        
        # Primero añadir al grupo
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        
        # Luego marcar como online y notificar a todos
        await self.mark_online(True)
        await self.accept()
        
        # Enviar lista actualizada a todos los usuarios
        await self.notify_all_users()

    async def disconnect(self, close_code):
        if hasattr(self, 'user_id'):
            await self.mark_online(False)
            await self.notify_all_users()
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    @database_sync_to_async
    def mark_online(self, is_online):
        User = get_user_model()
        try:
            user = User.objects.get(id=self.user_id)
            user.is_online = is_online
            user.last_activity = timezone.now()
            user.save(update_fields=['is_online', 'last_login'])  # Corregido last_login a last_activity
            return user
        except User.DoesNotExist:
            return None

    async def notify_all_users(self):
        users = await self.get_online_users()
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'broadcast_users',
                'users': users
            }
        )

    @database_sync_to_async
    def get_online_users(self):
        User = get_user_model()
        users = User.objects.filter(is_online=True).values(
            'id', 'username', 'first_name', 'last_name', 'is_online'
        )
        
        # Manejar casos donde no hay nombre o apellido
        return [
            {
                'id': u['id'],
                'username': u['username'],
                'fullname': self._get_user_fullname(u),
                'is_online': u['is_online']
            }
            for u in users
        ]
    
    def _get_user_fullname(self, user_data):
        first_name = user_data['first_name'] or ''
        last_name = user_data['last_name'] or ''
        
        # Obtener primer nombre y apellido si existen
        first_part = first_name.split()[0] if first_name else ''
        last_part = last_name.split()[0] if last_name else ''
        
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
        # Enviar lista completa de usuarios a todos los clientes
        await self.send(text_data=json.dumps({
            'type': 'online_users',
            'users': event['users']
        }))