import dj_database_url
from os import environ
from urllib.parse import urlparse
from ..utils import create_filename

from .base import *

ENV = 'stag'

ALLOWED_HOSTS = [
    'daat-hamakom-data-staging.herokuapp.com'
]

DATABASES = {
    'default': dj_database_url.config()
}

SECRET_KEY = environ.get('DJANGO_SECRET_KEY')

BROKER_URL = REDIS_URL = environ.get('REDIS_URL')
redis_url = urlparse(REDIS_URL)

CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        'LOCATION': 'redis://{}:{}'.format(redis_url.hostname, redis_url.port),
        'OPTIONS': {
            # "CLIENT_CLASS": "django_redis.client.HerdClient",
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
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

INSTALLED_APPS += (
    's3direct',
)

CELERY_ALWAYS_EAGER = False

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
STATIC_ROOT = str(PROJECT_DIR / 'staticroot')
STATIC_URL = '/static/'

RAVEN_CONFIG = {
    'dsn': environ.get('RAVEN_DSN')
}

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = environ.get('AWS_BUCKET_NAME')

S3DIRECT_REGION = 'eu-west-1'
S3DIRECT_DESTINATIONS = {
    'import-zip': (create_filename('import'), lambda u: u.is_authenticated(), ['application/zip', 'application/octet-stream']),
    'import-csv': (create_filename('import'), lambda u: u.is_authenticated(), ['text/csv']),
    'media': (create_filename('media'), lambda u: u.is_authenticated()),
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 86400  # this also enables the HSTS header
