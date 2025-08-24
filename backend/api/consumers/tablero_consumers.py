# consumers.py - CORREGIDO
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from api.dimon.models import Tablero
from api.dimon.serializers import TableroSerializer

class TableroConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'tableros'
        
        # Unirse al grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        print(f"WebSocket conectado: {self.channel_name}")  # Debug

    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"WebSocket desconectado: {self.channel_name}")  # Debug

    # Los métodos deben llamarse exactamente como los types que envías
    async def tablero_created(self, event):
        print("Evento tablero_created recibido:", event)  # Debug
        tablero_data = event['tablero_data']
        await self.send(text_data=json.dumps({
            'type': 'TABLERO_CREATED',
            'tablero': tablero_data
        }))
    
    async def tablero_updated(self, event):
        print("Evento tablero_updated recibido:", event)  # Debug
        tablero_data = event['tablero_data']
        await self.send(text_data=json.dumps({
            'type': 'TABLERO_UPDATED',
            'tablero': tablero_data
        }))
    
    async def tablero_deleted(self, event):
        print("Evento tablero_deleted recibido:", event)  # Debug
        tablero_id = event['tablero_id']
        await self.send(text_data=json.dumps({
            'type': 'TABLERO_DELETED',
            'id': tablero_id
        }))
    
    async def tablero_status_changed(self, event):
        print("Evento tablero_status_changed recibido:", event)  # Debug
        tablero_data = event['tablero_data']
        await self.send(text_data=json.dumps({
            'type': 'TABLERO_STATUS_CHANGED',
            'tablero': tablero_data
        }))