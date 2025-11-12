import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message 
from profiles.models import UserProfile
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from django.core.cache import cache
import redis.asyncio as aioredis
from django.utils.timezone import localtime
from channels.db import database_sync_to_async

import re #Expresiones regulares

REDIS_URL = "redis://127.0.0.1:6379"

# -- DB Helpers --
@database_sync_to_async
def get_user_profile(username):
    try:
        return UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist:
        return None

@database_sync_to_async
def get_room(room_id):
    try:
        return ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        return None

@database_sync_to_async
def create_message(sender_profile, room, content):
    message = Message.objects.create(
        sender=sender_profile, 
        room=room, 
        content=content
    )

    return message, message.sender.user.username


class ChatConsumer(AsyncWebsocketConsumer):
    get_user_profile = get_user_profile
    get_room = get_room
    create_message = create_message

    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"
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

        sender_profile = await get_user_profile(sender_username)
        room = await get_room(self.room_id)

        if sender_profile and room:
            message, username = await create_message(sender_profile, room, message_content)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message.content,
                    "username": username,
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
