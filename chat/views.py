from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from django.views.generic import TemplateView
from profiles.models import UserProfile
from django.core.serializers import serialize

class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ChatRoomsView(TemplateView):
    template_name = 'chat/chat_rooms.html'

    def get_queryset(self):
        # Obtener todos los chats en los que participa el usuario actual
        chatrooms = ChatRoom.objects.filter(users=self.request.user.profile)

        # Paso 1: Obtener los IDs de los perfiles de usuario que están en los chats del usuario actual
        chatted_profiles = UserProfile.objects.filter(chatroom__users=self.request.user.profile).values_list('id', flat=True)

        # Paso 2: Obtener todos los perfiles de usuario que no están en `chatted_profiles` y no incluir el propio perfil
        no_chatted_profiles = UserProfile.objects.exclude(id__in=chatted_profiles).exclude(id=self.request.user.profile.id)
        return chatrooms, no_chatted_profiles
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat_rooms'], context['no_chatted_profiles'] = self.get_queryset()
        return context
        
class ChatView(TemplateView):
    template_name = 'chat/chat.html'
    slug_field = 'room_id'
    slug_url_kwarg = 'room_id'
    
    def get_queryset(self):
        messages = Message.objects.filter(room=self.kwargs['room_id'])
        chatrooms = ChatRoom.objects.filter(users=self.request.user.profile)
        profiles = UserProfile.objects.filter(user__profile__in=ChatRoom.objects.get(id=self.kwargs['room_id']).users.all())

        return messages, chatrooms, profiles
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = ChatRoom.objects.get(id=self.kwargs['room_id'])

        usernames = room.users.exclude(
            id=self.request.user.profile.id
        ).values_list('user__username', flat=True)

        context['room_name'] = room.name # Nombre para conectar el websocket
        context['room_usernames'] = list(usernames) # Lista de usuarios del chat

        context['chat_messages'], context['chat_rooms'], context['profiles'] = self.get_queryset()
        return context

def create_chat_room(request, profile_id):
    sender_profile = request.user.profile  # Perfil del usuario autenticado
    receiver_profile = get_object_or_404(UserProfile, id=profile_id)  # Perfil del destinatario

    # Buscar si ya existe un chat privado entre ambos usuarios
    chatroom = ChatRoom.objects.filter(users=sender_profile).filter(users=receiver_profile).first()

    if not chatroom:
        # Si no existe, crea una nueva sala con ambos usuarios
        chatroom = ChatRoom.objects.create(name=f'{sender_profile.user.username}-{receiver_profile.user.username}')
        chatroom.users.add(sender_profile, receiver_profile)

    return redirect('chat:chat', room_id=chatroom.id)