from __future__ import absolute_import

from celery import Celery
from django.conf import settings
from os import environ

try:
    from raven import Client
    from raven.contrib.celery import register_signal
except ImportError:
    pass

environ.setdefault('DJANGO_SETTINGS_MODULE', 'daat.settings')

app = Celery('daat')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

RAVEN_DSN = environ.get('RAVEN_DSN')
if RAVEN_DSN:
    raven_client = Client(RAVEN_DSN)
    register_signal(raven_client)
