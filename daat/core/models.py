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


class Media(models.Model):

    MEDIA_CATEGORIES = (
        ('manuscript', 'Manuscript'),
        ('music_score', 'Music Score'),
        ('song', 'Song'),
        ('story', 'Story'),
        ('photograph', 'Photograph')
    )

    file = models.FileField()
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=50, choices=MEDIA_CATEGORIES)
    source = models.CharField(max_length=200, blank=True)
    source_url = models.CharField(max_length=500, blank=True)
    copyrights = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title


class Person(models.Model):
    title = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=120)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=150)
    nickname = models.CharField(max_length=150, blank=True)
    birth_date = models.CharField(max_length=10, validators=[partial_date_validator])
    death_date = models.CharField(max_length=10, blank=True, validators=[partial_date_validator])
    biography = models.TextField(blank=True)
    profile_image = models.ForeignKey(Media, blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def clean(self):
        if self.death_date:
            if self.death_date < self.birth_date:
                raise ValidationError({'death_date': 'Death date must occur after birth date'})


class Organization(models.Model):
    name = models.CharField(max_length=150)
    alt_name = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    places = ManyToManyField(Place, related_name='organizations')
    cover_image = models.ForeignKey(Media, blank=True, null=True)
    start_date = models.CharField(max_length=10, validators=[partial_date_validator])
    end_date = models.CharField(max_length=10, blank=True, validators=[partial_date_validator])

    def __str__(self):
        return self.name

    def clean(self):
        if self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({'end_date': 'End date must occur after start date'})


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
