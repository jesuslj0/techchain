from .base import *
import os
from pathlib import Path
from dotenv import load_dotenv

# Carga explícita del .env
ENV_PATH = Path(__file__).resolve().parent.parent / "app" / ".env"
load_dotenv(dotenv_path=ENV_PATH)


DEBUG = False
SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = ["techchain.live", "www.techchain.live"]

#Static
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Base de datos de producción
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ["DB_NAME"],
        'USER': os.environ["DB_USER"],
        'PASSWORD': os.environ["DB_PASSWORD"],
        'HOST': os.environ.get("DB_HOST", "localhost"),
        'PORT': os.environ.get("DB_PORT", "5432"),
    }
}


# Seguridad y caché
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Header para Google Auh
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Opcional: forzar HTTPS en producción
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

LOG_DIR = BASE_DIR / "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} [{name}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file_auth": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "auth.log"),
            "formatter": "verbose",
        },
        "file_error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "error.log"),
            "formatter": "verbose",
        },
    },
    "loggers": {
        # Logs de Django
        "django": {
            "handlers": ["console", "file_error"],
            "level": "WARNING",
            "propagate": True,
        },
        # Logs de autenticación (login, logout, fallos)
        "django.auth": {
            "handlers": ["console", "file_auth"],
            "level": "INFO",
            "propagate": False,
        },
        # Logs de seguridad (CSRF, permisos, etc.)
        "django.security": {
            "handlers": ["console", "file_error"],
            "level": "WARNING",
            "propagate": False,
        },
        # Logs generales del proyecto
        "techchain": {
            "handlers": ["console", "file_error"],
            "level": "INFO",
            "propagate": True,
        },
    },
}