from django.contrib import admin
from .models import User, UserProfile, Follow
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'uuid', 'username', 'last_login', 'date_joined', 'is_active', 'is_staff']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth_date']
    

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'followed', 'follow_up_date']
