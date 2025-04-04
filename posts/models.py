from django.db import models
from django.contrib.auth.models import User
from prose.fields import RichTextField

# Create your models here.

class Tag(models.Model):
    class TagChoices(models.TextChoices):
        TECNOLOGIA = "tecnologia", "Tecnología"
        SOFTWARE = "software", "Software"
        IA = "ia", "Inteligencia Artificial"
        DESARROLLO_WEB = "desarrollo_web", "Desarrollo Web"
        BACKEND = "backend", "Backend"
        FRONTEND = "frontend", "Frontend"
        BLOCKCHAIN = "blockchain", "Blockchain"
        BITCOIN = "BTC", "Bitcoin"

    name = models.CharField(
        max_length=20,
        choices=TagChoices.choices,
        unique=True
    )

    def __str__(self):
        return self.get_name_display() 

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Usuario')
    image = models.ImageField(upload_to='posts/posts_images/', verbose_name='Imagen')
    title = models.TextField(max_length=500, blank=False, verbose_name='Titulo')
    content = RichTextField(verbose_name='Contenido')
    tags = models.ManyToManyField('Tag', related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True, verbose_name='Nº de Likes')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

    def like(self, user):
        self.likes.add(user)

    def unlike(self, user):
        self.likes.remove(user)

class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name='Post al que pertenece el comentario', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, verbose_name='Autor', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Contenido del comentario', max_length=300)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['-created_at']

    def __str__(self):
        return f"Coméntó {self.user.username} en {self.post}"
    

