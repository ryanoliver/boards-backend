import os

from . import env_var
from .base import *


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bb!onz3e2hc1l-192ug40g@ykf^3@e4rtl!t9(i)d7n#oeo^!r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += (
    'django_extensions',
    'debug_toolbar',
)


DEBUG_TOOLBAR_PATCH_SETTINGS = env_var('DEBUG_TOOLBAR_PATCH_SETTINGS', True)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'boards',
        'USER': os.getenv('USER'),
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Django REST framework
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'blimp_boards.users.authentication.JWTAuthentication',
    'rest_framework.authentication.SessionAuthentication',
)

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)

JWT_AUTH = {
    'JWT_PAYLOAD_HANDLER': 'blimp_boards.utils.jwt_handlers.jwt_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=90)
}


# CORS Headers
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8000',
    'localhost:8000',
    'localhost:3333',
)


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     }
# }
