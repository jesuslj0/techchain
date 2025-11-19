from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile
from django.template.loader import render_to_string
from django.core.mail import send_mail
import logging

logger =  logging.getLogger(__name__)

User = get_user_model()

@receiver(post_save, sender=User)
def handle_user_creation_tasks(sender, instance, created, **kwargs):

    if created:
        # --- Cración del UserProfile
        UserProfile.objects.create(user=instance)

        # --- Envío del Correo de Bienvenida ---
        try:
            context = {'user': instance}
            html_message = render_to_string('emails/register_message.html', context)

            send_mail(
                subject="Bienvenido a TechChain",
                message="Gracias por registrarte en nuestra plataforma.",
                from_email="servicio.usuarios@techchain.live",
                recipient_list=[instance.email],
                fail_silently=True, # Cambio temporal
                html_message=html_message
            )
            
        except Exception as e:
            logger.error(f"Fallo de SMTP al enviar correo de bienvenida a {instance.email}. Error: {e}", exc_info=True)

