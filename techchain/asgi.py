"""
ASGI config for instagram project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techchain.settings")
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns  # Rutas de WebSockets
from channels.auth import AuthMiddlewareStack


application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,  # Peticiones HTTP normales
        "websocket": AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)  # Maneja WebSockets
        ),
    }
)

