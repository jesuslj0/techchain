from django.contrib import admin

# Register your models here.
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'receiver', 'message', 'timestamp']
    search_fields = ['sender', 'receiver']
    list_filter = ['timestamp']
    list_per_page = 10