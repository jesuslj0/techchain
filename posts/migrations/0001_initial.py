# Generated by Django 5.1.3 on 2025-01-31 02:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('tecnologia', 'Tecnología'), ('software', 'Software'), ('ia', 'Inteligencia Artificial'), ('desarrollo_web', 'Desarrollo Web'), ('backend', 'Backend'), ('frontend', 'Frontend'), ('blockchain', 'Blockchain'), ('BTC', 'Bitcoin')], max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='posts/posts_images/', verbose_name='Imagen')),
                ('title', models.TextField(blank=True, max_length=500, verbose_name='Titulo')),
                ('content', models.TextField(blank=True, verbose_name='Contenido')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('likes', models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL, verbose_name='Nº de Likes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('tags', models.ManyToManyField(related_name='posts', to='posts.tag')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=300, verbose_name='Contenido del comentario')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post', verbose_name='Post al que pertenece el comentario')),
            ],
            options={
                'verbose_name': 'Comentario',
                'verbose_name_plural': 'Comentarios',
                'ordering': ['-created_at'],
            },
        ),
    ]
