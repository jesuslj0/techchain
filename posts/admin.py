from django.contrib import admin
from .models import Post, Comment, Tag

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'title', 'content']
    autocomplete_fields = ['tags'] #Para una gran cantidad de tags

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']  # Permite buscar tags por nombre en el admin

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'text', 'post', 'created_at']