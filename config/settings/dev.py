from .base import *

import os

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '3@6wj-yed8gs+1^cr@$53xiox1=m*!!smls%i-zo2f-ob8r*v6')
ALLOWED_HOSTS = ["*"]
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME', 'locsharing'),
        'HOST': os.environ.get('DATABASE_HOST', '127.0.0.1'),
        'USER': os.environ.get('DATABASE_USER', 'dev'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'secret'),
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
    }
}

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {name} {pathname} {lineno:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'verbose'
        },
        'consumer': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        's6': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'verbose',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'apps': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'propagate': False,
        },
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        #     'propagate': False,
        # }
   },
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}
