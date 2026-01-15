from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password2 = serializers.CharField(write_only=True,  required=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2'
        ]
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Ya existe una cuenta vinculada a este email.")
        return value 

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    user = serializers.ReadOnlyField()

    def validate(self, data):
        username_or_email = data.get('username_or_email')
        password = data.get('password')
        
        if not username_or_email or not password:
            raise serializers.ValidationError(_("Debe proporcionar tanto el nombre de usuario/email como la contraseña."))

        user = authenticate(
            request=self.context.get('request'), 
            email=username_or_email, 
            password=password
        )
        
        if not user:
            user = authenticate(
                request=self.context.get('request'), 
                username=username_or_email, 
                password=password
            )

        if not user:
            raise serializers.ValidationError(_("Credenciales no válidas."))

        if not user.is_active:
            raise serializers.ValidationError(_("La cuenta de usuario está inactiva."))

        data['user'] = user
        return data

