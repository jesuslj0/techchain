# Funciones para crear y eliminar notificaciones
from .models import Notification

def create_notification(profile, type, message, link=None):
    new_notification = Notification.objects.create(profile=profile, type=type, message=message, link=link)
    new_notification.save()
    return new_notification

# Añadir funcionalidades