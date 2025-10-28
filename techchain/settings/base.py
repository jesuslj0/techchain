from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition
INSTALLED_APPS = [
    'daphne', #Servidor ASGI
    'channels', #Canal de comunicación
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'debug_toolbar',
    'crispy_forms',
    'crispy_bootstrap5',
    'prose',
    'rest_framework',
    
    'techchain',
    'profiles',
    'posts',
    'chat',
    'notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'techchain.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'techchain' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'techchain.context_processors.user_profile_context',
            ],
        },
    },
]

#Conexión que permite websockets
ASGI_APPLICATION = 'techchain.asgi.application'

# Configurar Redis como "message broker" para WebSockets
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],  # Servidor Redis local
        },
    },
}

AUTH_USER_MODEL = 'profiles.User'  # Modelo de usuario personalizado
LOGIN_REDIRECT_URL = '/'  # Redirige después del inicio de sesión exitoso
LOGOUT_REDIRECT_URL = 'logout'  # Redirige después del cierre de sesión

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'es-ES'
TIME_ZONE = 'Europe/Madrid'
USE_TZ = True
USE_I18N = True
USE_L10N = True


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email configuration Zoho Mail
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.zoho.eu"
EMAIL_PORT = 587  # Puerto correcto para TLS
EMAIL_USE_TLS = True  # Usa TLS para la seguridad
EMAIL_HOST_USER = os.environ["ZOHO_MAIL_SERVICE"] # Tu dirección de correo Zoho
EMAIL_HOST_PASSWORD = os.environ["ZOHO_MAIL_PASSWORD"]  # Usa tu contraseña o la contraseña de aplicación si tienes 2FA activado
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Form Styles
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

