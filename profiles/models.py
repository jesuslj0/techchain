from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField('Imagen de perfil', upload_to='profiles/profile_pictures/', blank=True, null=True)
    bio = models.TextField('Biografía', max_length=500, blank=True, null=True)
    birth_date = models.DateField('Fecha de nacimiento', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', through='Follow')
    
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

