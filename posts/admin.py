from django.contrib import admin
from .models import Post, Comment, Tag, Reel, ReelComment

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

@admin.register(Reel)
class ReelAdmin(admin.ModelAdmin):
    search_fields = ['user', 'caption', 'created_at']
    list_display = ['user', 'caption', 'created_at']

@admin.register(ReelComment)
class ReelCommentAdmin(admin.ModelAdmin):
    list_display = ['reel', 'user', 'text']
    search_fields = ['user', 'created_at']