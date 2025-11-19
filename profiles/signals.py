from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile
from django.template.loader import render_to_string
from django.core.mail import send_mail
import logging
from .utils import send_welcome_email

logger =  logging.getLogger(__name__)

User = get_user_model()

@receiver(post_save, sender=User)
def handle_user_creation_tasks(sender, instance, created, **kwargs):

    if created:
        # --- Cración del UserProfile
        UserProfile.objects.create(user=instance)

        # --- Envío del Correo de Bienvenida 
        send_welcome_email(instance)

