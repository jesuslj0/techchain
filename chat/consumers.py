import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message 
from profiles.models import UserProfile
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from django.core.cache import cache
import redis.asyncio as aioredis
from django.utils.timezone import localtime

import re #Expresiones regulares

REDIS_URL = "redis://127.0.0.1:6379"

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{re.sub(r'[^a-zA-Z0-9]', '_', self.room_name.lower())}"
        self.user = self.scope['user']

        if self.user.is_authenticated:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

            # Guardar estado en Redis
            redis = await aioredis.from_url(REDIS_URL)
            await redis.hset("online_users", self.user.username, 1)
            await redis.close()

        # Notificar lista actualizada a todos en la sala
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "broadcast_online_users"}
        )

    async def disconnect(self, close_code):
        self.user = self.scope['user']

        if self.user.is_authenticated:
            # Eliminar de Redis
            redis = await aioredis.from_url(REDIS_URL)
            await redis.hdel("online_users", self.user.username)
            await redis.close()


            # Sacar del grupo
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Notificar lista actualizada a todos en la sala
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "broadcast_online_users"}
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data["message"]
        sender_username = data["username"]

        sender_profile = await self.get_user_profile(sender_username)
        room = await self.get_room(self.room_name)

        if sender_profile and room:
            message = await self.create_message(sender_profile, room, message_content)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message.content,
                    "username": message.sender.user.username,
                    "timestamp": localtime(message.timestamp).isoformat(),
                    "profile_picture": (
                        sender_profile.profile_picture.url
                        if sender_profile.profile_picture else None
                    ),
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_status(self, event):
        await self.send(text_data=json.dumps(event))

    async def broadcast_online_users(self, event):
        await self.send_online_users()

    async def send_online_users(self):
        redis = await aioredis.from_url(REDIS_URL)
        online_users = await redis.hkeys("online_users")
        online_users = [user.decode("utf-8") for user in online_users]
        await redis.close()

        await self.send(text_data=json.dumps({
            "type": "online_users",
            "users": online_users
        }))

    # --- DB helpers ---
    async def get_room(self, room_name):
        try:
            return await sync_to_async(ChatRoom.objects.get, thread_sensitive=True)(name=room_name)
        except ChatRoom.DoesNotExist:
            return None

    async def get_user_profile(self, username):
        User = get_user_model()
        try:
            user = await sync_to_async(User.objects.get, thread_sensitive=True)(username=username)
            return await sync_to_async(lambda: user.profile, thread_sensitive=True)()
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            return None

    async def create_message(self, sender, room, content):
        return await sync_to_async(Message.objects.create, thread_sensitive=True)(
            sender=sender,
            room=room,
            content=content
        )
