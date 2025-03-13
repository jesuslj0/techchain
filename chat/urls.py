from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, MessageViewSet
from .views import ChatRoomsView, ChatView

router = DefaultRouter()
router.register(r'rooms', ChatRoomViewSet)
router.register(r'messages', MessageViewSet)

app_name = 'chat'

urlpatterns = [
    path('api/', include(router.urls)),
    path('rooms/', ChatRoomsView.as_view(), name='chat_rooms'),
    path('rooms/<slug:room_id>/', ChatView.as_view(), name='chat')
]
