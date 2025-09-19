from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import ChatRoom, Message, GroupChatRoom
from .serializers import ChatRoomSerializer, MessageSerializer
from django.views.generic import TemplateView, CreateView
from profiles.models import UserProfile
from django.core.serializers import serialize
from django.urls import reverse_lazy
from django.contrib import messages

class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ChatRoomsView(TemplateView):
    template_name = 'chat/chat_rooms.html'

    def get_queryset(self):
        # Obtener solo los chats individuales en los que participa el usuario actual
        chat_rooms = ChatRoom.objects.filter(users=self.request.user.profile).exclude(
            id__in=GroupChatRoom.objects.values_list("id", flat=True)
            )
        
        # Paso 1: Obtener los IDs de los perfiles de usuario que están en los chats del usuario actual
        chatted_profiles = UserProfile.objects.filter(chatroom__users=self.request.user.profile).values_list('id', flat=True)

        # Paso 2: Obtener todos los perfiles de usuario que no están en `chatted_profiles` y no incluir el propio perfil
        no_chatted_profiles = UserProfile.objects.exclude(id__in=chatted_profiles).exclude(id=self.request.user.profile.id)

        # Obtener los chats grupales
        group_chats = GroupChatRoom.objects.filter(users=self.request.user.profile)

        return chat_rooms, no_chatted_profiles, group_chats
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['chat_rooms'], context['no_chatted_profiles'], context['group_chats'] = self.get_queryset()
        return context
        
class ChatView(TemplateView):
    template_name = 'chat/chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_id = self.kwargs['room_id']
        room = get_object_or_404(ChatRoom, id=room_id)

        context['room_name'] = room.name
        context['room_usernames'] = room.users.exclude(id=self.request.user.profile.id).values_list('user__username', flat=True)
        context['chat_messages'] = Message.objects.filter(room=room)
        context['chat_rooms'] = ChatRoom.objects.filter(users=self.request.user.profile).exclude(id__in=GroupChatRoom.objects.values_list("id", flat=True))
        context['group_chats'] = GroupChatRoom.objects.filter(users=self.request.user.profile)
        context['profiles'] = UserProfile.objects.filter(user__profile__in=room.users.all())
        return context
    
class GroupChatCreateView(CreateView):
    model = GroupChatRoom
    template_name = 'chat/group_chat_create.html'
    fields = ['name', 'description', 'users']
    success_url = reverse_lazy('chat:chat_rooms')

    def form_valid(self, form):
        form.fields['users'].queryset = self.request.user.profile.followers.all() | self.request.user.profile.following.all()
        form.instance.creator = self.request.user.profile
        
        group_chat_room = form.save()

        # Añadir el creador a los administradores
        group_chat_room.admins.add(self.request.user.profile)

        # Mensaje de creación
        messages.add_message(self.request, messages.INFO, 'Grupo creado correctamente.')
        return super().form_valid(form)


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

