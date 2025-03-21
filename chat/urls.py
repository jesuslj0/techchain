from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, MessageViewSet
from .views import ChatRoomsView, ChatView, create_chat_room, GroupChatCreateView

router = DefaultRouter()
router.register(r'rooms', ChatRoomViewSet)
router.register(r'messages', MessageViewSet)

app_name = 'chat'

urlpatterns = [
    path('api/', include(router.urls)),
    path('rooms/', ChatRoomsView.as_view(), name='chat_rooms'),
    path('rooms/new-group/', GroupChatCreateView.as_view(), name='new_group_chat'), # Poner primero rutas sin slug o id para evitar fallos
    path('rooms/new/<int:profile_id>', create_chat_room, name='new_chat'), 
    path('rooms/<slug:room_id>/', ChatView.as_view(), name='chat'),
]
