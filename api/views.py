from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework.throttling import AnonRateThrottle

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,) # Permite acceso sin autenticación a todos los usuarios nuevos.
    throttle_classes = (AnonRateThrottle,) # Aplicar throttle

class CustomLoginView(APIView):
    serializer_class = LoginSerializer
    token_serializer = TokenObtainPairSerializer

    def post(self, request):
        # 1. Validar credenciales
        login_serializer = self.serializer_class(data=request.data, context={'request': request})
        login_serializer.is_valid(raise_exception=True)
        user = login_serializer.validated_data['user']

        # 2. Generar tokens
        token_data = {'username': user.username, 'password': request.data['password']}
        token_generator = self.token_serializer(data=token_data)
        token_generator.is_valid(raise_exception=True)

        return Response(
            token_generator.validated_data, status=status.HTTP_200_OK
        )

class PingView(APIView):
    def get(self, request):
        return Response({"status": "ok", "message": "pong"})