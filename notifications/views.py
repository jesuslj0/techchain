from django.shortcuts import render
from django.views.generic import ListView
from .models import Notification

# Create your views here.
class NotificationListView(ListView):
    model = Notification
    template_name = 'notifications/notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        all_notifications = super().get_queryset().filter(profile=self.request.user.profile)
        unread_notifications = all_notifications.filter(is_read=False)
        unread_notifications.update(is_read=True)
        return all_notifications
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['likes'] = self.get_queryset().filter(type='like')
        context['comments'] = self.get_queryset().filter(type='comment')
        context['posts'] = self.get_queryset().filter(type='post')
        context['follows'] = self.get_queryset().filter(type='follow')
        return context 
        
        
    