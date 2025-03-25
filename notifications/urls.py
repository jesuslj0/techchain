from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import NotificationListView

app_name = 'notifications'

urlpatterns = [
    path('list/', login_required(NotificationListView.as_view()), name='list',),
]
