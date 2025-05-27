# Funciones para crear y eliminar notificaciones
from .models import Notification

def create_notification(profile, type, post, message, link=None):
    try:
        new_notification = Notification.objects.create(profile=profile, type=type, post=post, message=message, link=link)
        new_notification.save()
    except Exception as e:
        new_notification.delete()
        print('NO se creó la notificación.', e.__cause__)
        raise BaseException(e)
    return new_notification

# Añadir funcionalidades