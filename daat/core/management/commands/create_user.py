import string
import random

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError

from daat.core.models import *


class Command(BaseCommand):
    help = 'Creates new users'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('first_name', type=str)
        parser.add_argument('last_name', type=str)
        parser.add_argument('email', type=str)


    def handle(self, *args, **options):
        user = DaatUser(username=options['username'], first_name=options['first_name'],
            last_name=options['last_name'], email=options['email'], is_staff=True)
        user.save()

        password = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(10)])
        user.set_password(password)
        user.save()

        group = Group.objects.get(name='Content Admins')
        group.user_set.add(user)
        group.save()

        print('{} {}'.format(options['username'], password))
