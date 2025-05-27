from django.db import models
from profiles.models import UserProfile
from django.contrib.auth.models import User
from posts.models import Post
from django.utils import timezone

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
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField(blank=False, null=False)
    link = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta: 
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'

    def __str__(self):
        return f'Notificación para {self.profile.user.username} - {self.message}'
    
class LikeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post')