from .base import *

ENV = 'local'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'daat',
    }
}

STATIC_ROOT = str(PROJECT_DIR / 'staticroot')
STATIC_URL = '/static/'
MEDIA_ROOT = str(PROJECT_DIR / 'media')
MEDIA_URL = '/media/'

CELERY_ALWAYS_EAGER = True
