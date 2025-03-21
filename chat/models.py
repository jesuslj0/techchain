from django.db import models
from profiles.models import UserProfile
from uuid import uuid4

class ChatRoom(models.Model):
    id = models.CharField(max_length=255, primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(UserProfile)

    class Meta:
        verbose_name = 'Sala de Chat'
        verbose_name_plural = 'Salas de Chat'

class GroupChatRoom(ChatRoom):
    description = models.TextField(max_length=500)
    admins = models.ManyToManyField(UserProfile)

    class Meta:
        verbose_name = 'Grupo de Chat'
        verbose_name_plural = 'Grupos de Chat'

class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender')
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='room')
    content = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'

    def __str__(self):
        return f'{self.sender} to {self.room}'