from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")
# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

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
    # Requeridos para allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Proveedor de Google
    'allauth.socialaccount.providers.google',

    'django_extensions',
    'debug_toolbar',
    'crispy_forms',
    'crispy_bootstrap5',
    'prose',
    'rest_framework',
    'corsheaders',
    
    'techchain',
    'profiles',
    'posts',
    'chat',
    'notifications',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    # Middleware custom
    'techchain.middleware.profile_completion.ProfileCompletionMiddleware',

    # Allauth
    'allauth.account.middleware.AccountMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    #Ayuda a seguridad en producción
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        # Limita las solicitudes de usuarios no autenticados (Anónimos)
        'anon': '100/day', # 100 registros al día por IP
        'register': '3/minute', # Máximo 3 intentos de registro por minuto por IP
    },
}

CORS_ALLOW_ALL_ORIGINS = True

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
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

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


# Allauth
AUTHENTICATION_BACKENDS = [
    # Requerido para iniciar sesión como administrador
    'django.contrib.auth.backends.ModelBackend',
    # allauth para autenticación
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Google AllAuth
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "openid",
            "email",
            "profile",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        }
    }
}

SITE_ID = 1 # django.contrib.sites

# Configuraciones específicas de allauth
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_UNIQUE_EMAIL = True

SOCIALACCOUNT_PROVIDERS['google']['APP'] = {
    'client_id': os.getenv("SOCIAL_AUTH_GOOGLE_CLIENT_ID"),
    'secret': os.getenv("SOCIAL_AUTH_GOOGLE_CLIENT_SECRET"),
    'key': '',
}

# Configuracion de logging con Sentry
import sentry_sdk

SENTRY_DSN = os.environ.get("SENTRY_DSN")

sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=0.2,
    send_default_pii=True,
)

PROFILE_EXCLUDE_URLS = ['/accounts/']