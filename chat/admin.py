from django.contrib import admin
from .models import ChatRoom, Message  

# Register your models here.
@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_per_page = 10

@admin.register(Message)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['sender', 'room', 'content', 'timestamp']
    search_fields = ['sender', 'room', 'content']
    list_filter = ['timestamp']
    list_per_page = 10