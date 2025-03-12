from django.db import models
from profiles.models import UserProfile

class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(UserProfile)

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