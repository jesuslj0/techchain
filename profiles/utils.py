from django.core.mail import send_mail
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

def send_welcome_email(user_instance):
    """Intenta enviar el correo de bienvenida, silenciando fallos."""
    try:
        context = {'user': user_instance}
        html_message = render_to_string('emails/register_message.html', context)

        send_mail(
            subject="Bienvenido a TechChain",
            message="Gracias por registrarte en nuestra plataforma.",
            from_email="servicio.usuarios@techchain.live",
            recipient_list=[user_instance.email],
            fail_silently=True, 
            html_message=html_message
        )
    except Exception as e:
        logger.error(f"Error crítico no silenciado al preparar el correo para {user_instance.email}: {e}")