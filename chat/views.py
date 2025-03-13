from django.shortcuts import render
from rest_framework import viewsets
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from django.views.generic import TemplateView

class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ChatRoomsView(TemplateView):
    template_name = 'chat/chat_rooms.html'
    context_object_name = 'chat_rooms'

    def get_queryset(self):
        return ChatRoom.objects.filter(users=self.request.user.profile)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat_rooms'] = self.get_queryset()
        return context
        
class ChatView(TemplateView):
    template_name = 'chat/chat.html'
    slug_field = 'room_id'
    slug_url_kwarg = 'room_id'
    
    def get_queryset(self):
        messages = Message.objects.filter(room=self.kwargs['room_id'])
        chatrooms = ChatRoom.objects.filter(users=self.request.user.profile)
        return messages, chatrooms
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_name'] = ChatRoom.objects.get(id=self.kwargs['room_id']).name 
        context['chat_messages'], context['chat_rooms'] = self.get_queryset()
        return context
