from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError

from daat.maps.utils import SpriteCreator
from daat.maps.models import *


class Command(BaseCommand):
    help = 'Generates the sprites image and data'

    def handle(self, *args, **options):
        sc = SpriteCreator(Event.objects.all())
        sc.build()

        cache.set('sprites:json', sc.json, 0)
        cache.set('sprites:png', sc.png, 0)
