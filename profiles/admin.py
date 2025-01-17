from django.contrib import admin
from .models import UserProfile, Follow
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth_date']
    

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'followed', 'follow_up_date']
