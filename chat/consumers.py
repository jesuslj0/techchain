import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message 
from profiles.models import UserProfile
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from django.core.cache import cache
import aioredis

REDIS_URL = "redis://127.0.0.1:6379"

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope['user']

        if self.user.is_authenticated:

            await self.channel_layer.group_add(self.room_group_name, self.channel_name) # Agregar el canal al grupo
            await self.accept() # Aceptar conexión

            # Guardar estado en Redis
            redis = await aioredis.from_url(REDIS_URL)
            await redis.hset("online_users", self.user.username, 1)  # 1 = Online
            await redis.close()

            # Notificar a todos que el usuario está online
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_status",
                    "user": self.user.username,
                    "is_online": True,
                },
            )

            # Enviar lista de usuarios online al conectarse
            await self.send_online_users()

    async def disconnect(self, close_code):
        self.user = self.scope['user']
        
        if self.user.is_authenticated:
            
            # Marcar usuario como offline en Redis
            redis = await aioredis.from_url(REDIS_URL)
            await redis.hdel("online_users", self.user.username)
            await redis.close()

            # Notificar a todos que el usuario está offline
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_status",
                    "user": self.user.username,
                    "is_online": False,
                },
            )

            await self.channel_layer.group_discard(self.room_group_name, self.channel_name) # Eliminar el canal del grupo

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data["message"]
        sender_username = data["username"]

        # Obtener el perfil del usuario en lugar del usuario directamente
        sender_profile = await self.get_user_profile(sender_username)
        room = await self.get_room(self.room_name)

        if sender_profile and room:
            message = await self.create_message(sender_profile, room, message_content)

            # Enviar el mensaje a todos los usuarios en la sala
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message.content,
                    "username": message.sender.user.username,  
                    "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

    async def chat_message(self, event):
        # Recibir mensaje del grupo y enviarlo a WebSocket
        await self.send(text_data=json.dumps(event))
    
    # Funciones para consultar la base de datos 
    async def get_room(self, room_name):
        try:
            return await sync_to_async(ChatRoom.objects.get, thread_sensitive=True)(name=room_name)
        except ChatRoom.DoesNotExist:
            return None
        
    async def get_user_profile(self, username):
        User = get_user_model()
        try:
            user = await sync_to_async(User.objects.get, thread_sensitive=True)(username=username)
            profile = await sync_to_async(lambda: user.profile, thread_sensitive=True)()  # Obtenemos el Profile
            return profile
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            return None
        
    async def create_message(self, sender, room, content):
        return await sync_to_async(Message.objects.create, thread_sensitive=True)(
            sender=sender, 
            room=room, 
            content=content
        )
    
    # async def set_user_online(self, user, is_online=True):
    #     # Guardar el estado del usuario en la caché
    #     cache.set(f"user_status_{user.id}", is_online)

    # async def set_user_offline(self, user):
    #     # Eliminar el estado del usuario de la caché
    #     cache.delete(f"user_status_{user.id}")

    async def user_status(self, event):
        # Se necesita para manejar el type user_status
        await self.send(text_data=json.dumps(event))

    async def send_online_users(self):
    # Recuperar la lista de usuarios online
        redis = await aioredis.from_url(REDIS_URL)
        online_users = await redis.hkeys("online_users")  # Lista de usuarios online
        
        # Decodificar bytes a strings
        online_users = [user.decode('utf-8') for user in online_users]

        await redis.close()

        await self.send(text_data=json.dumps({"type": "online_users", "users": online_users}))

