from django.contrib import admin
from .models import ChatRoom, Message, GroupChatRoom  

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

class UsersInline(admin.TabularInline):
    model = GroupChatRoom.users.through
    extra = 1

class AdminsInline(admin.TabularInline):
    model = GroupChatRoom.admins.through
    extra = 1

@admin.register(GroupChatRoom)
class GroupChatRoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']

    inlines = [
        UsersInline, 
        AdminsInline
    ]
    
    list_per_page = 10