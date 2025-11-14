from django.db import models
from profiles.models import UserProfile
from django.conf import settings
from uuid import uuid4
from django.utils import timezone

class ChatRoom(models.Model):
    id = models.CharField(max_length=255, primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(UserProfile)

    class Meta:
        verbose_name = 'Sala de Chat'
        verbose_name_plural = 'Salas de Chat'

class GroupChatRoom(ChatRoom):
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_groups')
    description = models.TextField(max_length=500, blank=True)
    admins = models.ManyToManyField(UserProfile)
    image = models.FileField(verbose_name="Imagen de grupo", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Fecha de creación', default=timezone.now)

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