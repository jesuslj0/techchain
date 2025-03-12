from rest_framework import serializers
from .models import ChatRoom, Message

# Serializers define the API representation.
# Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes
# that can then be easily rendered into JSON, XML or other content types.
class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'  # Incluye todos los campos del modelo

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'  # Incluye todos los campos del modelo
