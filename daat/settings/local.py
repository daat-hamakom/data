from .base import *

ENV = 'local'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'daat',
    }
}

STATIC_ROOT = str(PROJECT_DIR / 'staticroot')
STATIC_URL = '/static/'
MEDIA_ROOT = str(PROJECT_DIR / 'media')
MEDIA_URL = '/media/'

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += ('rest_framework.renderers.BrowsableAPIRenderer',)

CELERY_ALWAYS_EAGER = True

STATICFILES_DIRS = [
    PROJECT_DIR.joinpath("static"),
]
