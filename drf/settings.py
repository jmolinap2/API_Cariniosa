"""
Django settings for drf project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m$1xiohbetxtnfa9%zaaxgp!uh7_r*xu(1e!s3h$)&c7_q--47'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

# Aplicaciones de Django contribuidas por Django
DJANGO_CONTRIB_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Aplicaciones de terceros
THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'coreapi',
    'corsheaders',  # CORS para permitir solicitudes desde otros dominios
    'drf_yasg',
]

# Tus propias aplicaciones personalizadas
MIS_APPS = [
    'api',
]

INSTALLED_APPS = DJANGO_CONTRIB_APPS + THIRD_PARTY_APPS + MIS_APPS


CORS_ORIGIN_WHITELIST = [
    'https://xf0hbthg-4200.brs.devtunnels.ms',
    'http://localhost:4200',  # Origen de tu aplicación Angular
    'http://127.0.0.1:4200',
    
]
CORS_ALLOWED_ORIGINS = [
    'https://xf0hbthg-4200.brs.devtunnels.ms',  
]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'drf.middleware.TokenAuthenticationMiddleware',
    'drf.middleware.RequestLoggingMiddleware',
]

ROOT_URLCONF = 'drf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'drf.wsgi.application'
AUTH_USER_MODEL = 'api.User'



# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Configuración por defecto sin el host
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'CarinosasAPI_db',
        'USER': 'postgres',
        'PASSWORD': '12345',
        'PORT': '5432',
    }
}

# Si se detecta que está corriendo dentro de Docker, añadir el host
if 'DOCKER_ENV' in os.environ:
    DATABASES['default']['HOST'] = 'db'


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

TOKEN_EXPIRED_AFTER_SECONDS = 80000
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

}

# Configuración específica para desarrollo
if DEBUG:
    REST_FRAMEWORK.update({
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.TokenAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
    })

# Configuración específica para producción, incluida la autenticación JWT
else:
    REST_FRAMEWORK.update({
        
    })


LOGTAIL_UPDATE_INTERVAL = 2000 # El valor predeterminado es 3000 (tres segundos)
# Configuración del registro
""" REST_FRAMEWORK.update({
    'DEFAULT_LOGGER': 'drf_logger',
    'LOGGING': {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'INFO',  # Adjust level as needed (e.g., DEBUG for more details)
                'class': 'logging.StreamHandler',
            },
            'file': {
                'level': 'DEBUG',  # Log all messages to the file
                'class': 'logging.FileHandler',
                'filename': './registro.log',
            },
        },
        'loggers': {
            'drf_logger': {
                'handlers': ['console', 'file'],  # Log to both console and file
                'level': 'DEBUG',  # Log all messages at DEBUG level
                'propagate': True,
            },
            'django': {
                'handlers': ['console', 'file'],  # Log to both console and file
                'level': 'DEBUG',  # Log all messages at DEBUG level
                'propagate': True,
            },
        },
    },
})
 """
