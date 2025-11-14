from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import ChatRoom, Message, GroupChatRoom
from .serializers import ChatRoomSerializer, MessageSerializer
from django.views.generic import TemplateView, CreateView, DetailView, DeleteView
from profiles.models import UserProfile
from django.core.serializers import serialize
from django.urls import reverse_lazy
from django.contrib import messages
from django.forms import forms
from .forms import GroupChatForm
from django.http import HttpResponseRedirect

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
        room_instance = None

        try:
            room_instance = GroupChatRoom.objects.get(id=room_id)
            context['is_group_chat'] = True
            context['display_name'] = room_instance.name
        except GroupChatRoom.DoesNotExist:
            room_instance = get_object_or_404(ChatRoom, id=room_id)
            context['is_group_chat'] = False

            other_profile = room_instance.users.exclude(id=self.request.user.profile.id).first()
            if other_profile:
                context['display_name'] = other_profile.user.username
            else:
                context['display_name'] = self.request.user.username 
            
            context['room_usernames'] = [context['display_name']]
            context['other_profile'] = other_profile
        
        context['chat_messages'] = Message.objects.filter(room=room_instance).order_by('timestamp')
        
        context['current_room'] = room_instance
        context['profiles'] = room_instance.users.all() # Lista de todos los perfiles en el chat
        
        context['chat_rooms'] = ChatRoom.objects.filter(users=self.request.user.profile).exclude(id__in=GroupChatRoom.objects.values_list("id", flat=True))
        context['group_chats'] = GroupChatRoom.objects.filter(users=self.request.user.profile)
        return context
    
class GroupChatCreateView(CreateView):
    model = GroupChatRoom
    template_name = 'chat/group_chat_create.html'
    form_class = GroupChatForm
    success_url = reverse_lazy('chat:chat_rooms')

    def get_form(self, form_class=None):
        allowed_users = self.request.user.profile.followers.all() | self.request.user.profile.following.all()
        return self.form_class(**self.get_form_kwargs(), allowed_users=allowed_users)
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user.profile
        # Save the form to create the GroupChatRoom instance
        self.object.save()
        
        # Add the creator as a user and admin
        self.object.users.add(self.request.user.profile)
        self.object.admins.add(self.request.user.profile)

        for user in form.cleaned_data['users']:
            self.object.users.add(user)

        messages.add_message(self.request, messages.INFO, f'Grupo "{self.object.name}" creado correctamente.')

        return HttpResponseRedirect(self.get_success_url())


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

class GroupDetailView(DetailView):
    model = GroupChatRoom
    template_name = "chat/group_detail.html"
    context_object_name = 'group'
    pk_url_kwarg = 'room_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat_messages'] = Message.objects.filter(room=self.object)
        return context

class GroupDeleteView(DeleteView):
    model = GroupChatRoom
    template_name = "chat/group_confirm_delete.html"
    success_url = reverse_lazy('chat:chat_rooms')
    context_object_name = 'group'
    pk_url_kwarg = 'group_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.creator != self.request.user.profile:
            messages.error(request, "No tienes permiso para borrar este grupo.")
            return HttpResponseRedirect(self.success_url)

        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Grupo eliminado correctamente.")
        return HttpResponseRedirect(success_url)