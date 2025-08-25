from datetime import timedelta
import os
from pathlib import Path
import config.db as db

AUTH_USER_MODEL = "user.User"


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Obtener la clave sin valor por defecto
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "True") == "True"
# Validación en producción
if not DEBUG and not SECRET_KEY:
    raise ValueError("SECRET_KEY no configurado - Configura la variable de entorno")

# Valor solo para desarrollo (opcional)
if DEBUG and not SECRET_KEY:
    SECRET_KEY = "django-insecure-dev-only-key"  # Solo para desarrollo local
    print("ADVERTENCIA: Usando clave de desarrollo insegura")
    
# si no hay ninguna variable se considera como TRUE
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# Application definition
BASE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "corsheaders",
    "django_filters",
    "channels",
    "django_redis",
    "simple_history",
]

OWN_APPS = [
    "api",
    'api.user.apps.UserConfig',  # ¡Importante el .apps.UserConfig!
    "api.gore",
    "api.dimon",
    "api.dgos.administracion",
    
]

INSTALLED_APPS = BASE_APPS + THIRD_APPS + OWN_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "config.middleware.SessionTimeoutMiddleware",  # Primero el de sesión
    #'config.middleware.CustomAuditMiddleware',    # Finalmente nuestro custom
    'middleware.middlewareAudit.JWTAuditMiddleware',    # Finalmente nuestro custom
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

# agregando q dominios locales para consumir la API
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost",
    "http://127.0.0.1:8080",
    "http://172.27.0.200:8080",
    "http://localhost:4000",
    "http://127.0.0.1:4000",
    "http://172.27.0.200:9900",
    "http://192.168.18.23:8080",
]

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=8),  # Token de acceso válido por 8 horas
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  # Token de refresco válido por 1 día
    "ROTATE_REFRESH_TOKENS": True,  # Genera nuevo token al refrescar
    "BLACKLIST_AFTER_ROTATION": True,  # Invalida tokens viejos
    "UPDATE_LAST_LOGIN": True,  # Actualiza última conexión del usuario
    "AUTH_HEADER_TYPES": ("Bearer",),  # Uso: "Bearer <token>"
}

# Configuración de DRF Spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "API Documentation",
    "DESCRIPTION": "Documentación de la API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_AUTHENTICATION": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "PREPROCESSING_HOOKS": [
        "drf_spectacular.hooks.preprocess_exclude_path_format",
    ],
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
    },
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAuthenticated"],
    "SERVE_AUTHENTICATION": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "COMPONENT_SPLIT_REQUEST": True,
    "SECURITY": [
        {"Bearer": []},  # Necesario para mostrar el botón "Authorize"
    ],
    "SECURITY_SCHEMES": {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    },
    "SCHEMA_VERSION": "3.1.1",
}


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],  # Añade esta línea
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DATABASES = db.DATABASES

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]



LANGUAGE_CODE = "es-pe"
TIME_ZONE = "America/Lima"
USE_I18N = True  # Habilita la internacionalización
USE_L10N = True  # Habilita la localización
USE_TZ = True  # Usa zona horaria

# Configuración adicional para formatos locales
DATE_FORMAT = "d/m/Y"
DATETIME_FORMAT = "d/m/Y H:i:s"
SHORT_DATE_FORMAT = "d/m/Y"
SHORT_DATETIME_FORMAT = "d/m/Y H:i"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

#
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


if not DEBUG:
    SECURE_HSTS_SECONDS = 3600  # 1 hora
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Configuración de seguridad para cookies
SESSION_COOKIE_AGE = 8 * 60 * 60  # 8 horas en segundos (8h * 60m * 60s)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Para respetar el tiempo de expiración
SESSION_SAVE_EVERY_REQUEST = True  # Renueva el tiempo de expiración con cada solicitud
SESSION_COOKIE_HTTPONLY = True  # Previene acceso via JavaScript
CSRF_COOKIE_HTTPONLY = False  # Debe ser False para que AJAX funcione
CORS_ALLOW_CREDENTIALS = True  # Importante para incluir cookies/autorización
# Configuración para desarrollo (ajusta según entorno)
if DEBUG:
    CSRF_COOKIE_SECURE = False  # False en desarrollo, True en producción
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SAMESITE = 'Lax'  # 'Lax' para desarrollo
    SESSION_COOKIE_SAMESITE = 'Lax'
else:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = 'Strict'
    SESSION_COOKIE_SAMESITE = 'Strict'
# Configuración adicional de seguridad
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CORS_EXPOSE_HEADERS = ['Set-Cookie']

if not DEBUG and os.getenv("AWS_ACCESS_KEY_ID"):
    # Configuración para AWS S3 en producción
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_DEFAULT_ACL = "public-read"
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
else:
    # Configuración para desarrollo
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ======================================
# Configuración de Channels y Redis
# ======================================
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

#CREAR DOCKERS CON CLAVE
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, int(REDIS_PORT))],
            "capacity": 1500,
            "expiry": 10,
        },
    },
}

# ======================================
# Configuración de Caché
# ======================================
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        },
    }
}

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/api/schema/swagger/"

# Opcional: Configuración adicional
SIMPLE_HISTORY_HISTORY_CHANGE_REASON_USE_TEXT_FIELD = True
SIMPLE_HISTORY_REVERT_DISABLED = False  # Permite revertir cambios


# PARA PRODUCCIÓN
#DEBUG = False
#SECURE_HSTS_SECONDS = 31536000  # 1 año
#SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#SECURE_HSTS_PRELOAD = True

# Configuración para proxy inverso
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Configuración para correo electrónico
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'bot.reporte.dimon@gmail.com'
EMAIL_HOST_PASSWORD = 'moeh ljtd xebl pibc'
DEFAULT_FROM_EMAIL  = 'bot.reporte.dimon@gmail.com'  # <-- Añade el remitente

FRONTEND_URL = 'http://localhost:8080'  # URL de tu frontend Vue.js en desarrollo