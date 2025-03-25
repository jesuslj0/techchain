from django.db import models
from profiles.models import UserProfile

# Create your models here.
class Notification(models.Model):
    class Type(models.TextChoices):
        LIKE = 'like'
        COMMENT = 'comment'
        POST = 'post'
        FOLLOW = 'follow'
        MESSAGE = 'message'
    
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.LIKE)
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'

    def __str__(self):
        return f'Notificación para {self.profile.user.username} - {self.message}'
    
