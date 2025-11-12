from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path(r"ws/chat/<str:room_id>/", ChatConsumer.as_asgi()),
]
