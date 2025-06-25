"""
ASGI config for instagram project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns  # Rutas de WebSockets
from channels.auth import AuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techchain.settings")
django.set_up() # IMPORTANTE PARA CARGAR DJANGO EN ASWI

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),  # Peticiones HTTP normales
        "websocket": AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)  # Maneja WebSockets
        ),
    }
)

