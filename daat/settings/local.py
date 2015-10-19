from .base import *

ENV = 'local'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'daat',
        'USER': 'daat',
        'PASSWORD': 'daat'
    }
}
