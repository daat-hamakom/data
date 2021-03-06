from .base import *
from os import environ
from ..utils import create_filename

ENV = 'local'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'daat',
    }
}


BROKER_URL = "redis://127.0.0.1:6379/0"
# Redis setup
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_CONNECT_RETRY = True
CELERY_SEND_EVENTS = True
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_TASK_RESULT_EXPIRES = 60
CELERY_ALWAYS_EAGER = False

INSTALLED_APPS += (
    's3direct',
)

AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = environ.get('AWS_BUCKET_NAME')
S3DIRECT_REGION = 'eu-west-1'


S3DIRECT_DESTINATIONS = {
    'import-zip': (create_filename('import'), lambda u: u.is_authenticated(), ['application/zip', 'application/octet-stream']),
    'import-csv': (create_filename('import'), lambda u: u.is_authenticated(), ['text/csv']),
    'media': (create_filename('media'), lambda u: u.is_authenticated()),
}

STATIC_ROOT = str(PROJECT_DIR / 'staticroot')
STATIC_URL = '/static/'
MEDIA_ROOT = str(PROJECT_DIR / 'media')
MEDIA_URL = '/media/'

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += ('rest_framework.renderers.BrowsableAPIRenderer',)

