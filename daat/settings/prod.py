import dj_database_url
from os import environ
from urllib.parse import urlparse

from .base import *

ENV = 'prod'

ALLOWED_HOSTS = [
    'daat-hamakom.herokuapp.com'
]

DATABASES = {
    'default': dj_database_url.config()
}

SECRET_KEY = environ.get('DJANGO_SECRET_KEY')

BROKER_URL = REDIS_URL = environ.get('REDISCLOUD_URL')
redis_url = urlparse(REDIS_URL)

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '{}:{}'.format(redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'DB': 0,
            'PASSWORD': redis_url.password,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 5,
                'timeout': 20
            }
        }
    }
}

CELERY_ALWAYS_EAGER = True

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
STATIC_ROOT = str(PROJECT_DIR / 'staticroot')
STATIC_URL = '/static/'

RAVEN_CONFIG = {
    'dsn': environ.get('RAVEN_DSN')
}

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)
