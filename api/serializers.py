from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from profiles.models import UserProfile 
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2'
        ]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Ya existe una cuenta vinculada a este email. Por favor, use otro distinto")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')

        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError("Credenciales inválidas.")
        return user

