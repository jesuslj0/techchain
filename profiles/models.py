from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid

# Usuario personalizado con uuid
class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField('Imagen de perfil', upload_to='profiles/profile_pictures/', blank=True, null=True)
    bio = models.TextField('Biografía', max_length=500, blank=True, null=True)
    birth_date = models.DateField('Fecha de nacimiento', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', through='Follow')
    last_password_change = models.DateTimeField('Último cambio de contraseña',  null=True, blank=True)  
    private = models.BooleanField('Perfil privado', default=False)

    class Meta:
        managed = True
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self) -> str:
        return self.user.username
    
class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, verbose_name='Seguidor', on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey(UserProfile, verbose_name='Seguido', on_delete=models.CASCADE, related_name='followed')
    follow_up_date = models.DateField(auto_now_add=True, verbose_name='Fecha de seguimiento')

    class Meta: 
        unique_together = ('follower', 'followed')
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'

    def __str__(self):
        return f'{self.follower} follows {self.followed}'



