from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import *


class EventTestCase(TestCase):
    def setUp(self):
        pass

    def test_event_dates(self):
        Event.objects.create(title='Test Event', start_date='2015-11-11', end_date='2015-12-12').full_clean()
        Event.objects.create(title='Test Event', start_date='2015-00-00', end_date='2016-00-00').full_clean()
        with self.assertRaises(ValidationError):
            Event.objects.create(title='Test Event', start_date='4444x02a00').full_clean()
        with self.assertRaises(ValidationError):
            Event.objects.create(title='Test Event', start_date='4444-02-00').full_clean()
        with self.assertRaises(ValidationError):
            Event.objects.create(title='Test Event', start_date='2015-00-22').full_clean()
        with self.assertRaises(ValidationError):
            Event.objects.create(title='Test Event', start_date='2015-02-30').full_clean()
        with self.assertRaises(ValidationError):
            Event.objects.create(title='Test Event', start_date='2015-02-30', end_date='2014-01-02').full_clean()

    def test_person_dates(self):
        with self.assertRaises(ValidationError):
            Person.objects.create(first_name='Shai', last_name='Agnon', birth_date='1999-09-09', death_date='1888-08-08')

    def test_organization_dates(self):
        with self.assertRaises(ValidationError):
            Event.objects.create(name='Test Org', start_date='2015-02-30', end_date='2014-01-02').full_clean()