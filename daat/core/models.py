from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from .utils import partial_date_validator


class DaatUser(AbstractUser):
    pass


class Project(models.Model):
    pass


class Place(models.Model):
    pass


class Person(models.Model):
    pass


class Organization(models.Model):
    pass


class Media(models.Model):
    pass


class Event(models.Model):
    MAP_CONTEXTS = (
        ('neighbourhood', 'Neighbourhood'),
        ('city', 'City'),
        ('province', 'Province'),
        ('country', 'Country'),
        ('continent', 'Continent'),
        ('world', 'World'),
    )

    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    start_date = models.CharField(max_length=10, validators=[partial_date_validator])
    end_date = models.CharField(max_length=10, blank=True, validators=[partial_date_validator])
    place = models.ForeignKey(Place, related_name='events')
    map_context = models.CharField(max_length=20, choices=MAP_CONTEXTS, blank=True)
    people = models.ManyToManyField(Person, related_name='events')
    organizations = models.ManyToManyField(Organization, related_name='events')
    media = models.ManyToManyField(Media, related_name='events')

    def __str__(self):
        return self.title

    def clean(self):
        if self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({'end_date': 'End date must occur after start date'})
