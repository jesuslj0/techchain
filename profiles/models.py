from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid

# Usuario personalizado con uuid
class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/profile_pictures/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Follow',
        through_fields=('followed', 'follower'),
        related_name='following'
    )
    last_password_change = models.DateTimeField(null=True, blank=True)
    private = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuarios"


class Follow(models.Model):
    follower = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='following_set')
    followed = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='followers_set')
    follow_up_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f'{self.follower} -> {self.followed}'

