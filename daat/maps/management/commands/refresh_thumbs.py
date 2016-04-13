from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError

from daat.maps.utils import SpriteCreator
from daat.maps.models import *
from daat.maps.tasks import gen_image_thumbnails

class Command(BaseCommand):
    help = 'Refresh image media thumbnails'

    def handle(self, *args, **options):
        for im in Media.objects.filter(type='image'):
            print(im)
            try:
                gen_image_thumbnails(im)
            except Exception as e:
                print(e)
