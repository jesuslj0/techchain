import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message 
from profiles.models import UserProfile
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Unir la sala del chat
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Salir de la sala
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data["message"]
        sender_username = data["username"]

        # Obtener el perfil del usuario en lugar del usuario directamente
        sender_profile = await self.get_user_profile(sender_username)
        room = await self.get_room(self.room_name)

        if sender_profile and room:
            message = await self.create_message(sender_profile, room, message_content)

            sender_username = await sync_to_async(lambda: message.sender.user.username)()

            # Enviar el mensaje a todos los usuarios en la sala
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message.content,
                    "username": sender_username,  
                    "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )


    async def chat_message(self, event):
        # Recibir mensaje del grupo y enviarlo a WebSocket
        message = event["message"]
        username = event["username"]
        timestamp = event["timestamp"]

        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
            "timestamp": timestamp,
        }))
    
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
    
