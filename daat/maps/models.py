from django.core.exceptions import ValidationError
from django.db import models
from geoposition.fields import GeopositionField

from .utils import partial_date_validator


def concat_category(i, f):
    return '{}/{}'.format(i.category, f)


class PartialDateCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        kwargs['validators'] = [partial_date_validator]
        kwargs['help_text'] = 'Date in YYYY-MM-DD format, use 00 to denote month/day ranges'
        return super().__init__(*args, **kwargs)


class Media(models.Model):

    MEDIA_CATEGORIES = (
        ('manuscript', 'Manuscript'),
        ('music_score', 'Music Score'),
        ('song', 'Song'),
        ('story', 'Story'),
        ('photograph', 'Photograph')
    )

    file = models.FileField(upload_to=concat_category)
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=50, choices=MEDIA_CATEGORIES)
    source = models.CharField(max_length=200, blank=True)
    source_url = models.CharField(max_length=500, blank=True)
    copyrights = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title


class Researcher(models.Model):
    title = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=150)
    biography = models.TextField(blank=True)
    profile_image = models.FileField(upload_to='researcher_profiles', blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Project(models.Model):
    title = models.CharField(max_length=150)
    researchers = models.ManyToManyField(Researcher, blank=True, related_name='projects')
    synopsis = models.TextField(blank=True)
    cover_image = models.ForeignKey(Media, blank=True, null=True)
    start_date = PartialDateCharField()
    end_date = PartialDateCharField(blank=True)

    def __str__(self):
        return self.title

    def clean(self):
        if self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({'end_date': 'End date must occur after start date'})


class Place(models.Model):
    name = models.CharField(max_length=200)
    alt_name = models.CharField(max_length=300, blank=True)
    position = GeopositionField()

    def __str__(self):
        return self.name


class Person(models.Model):
    title = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=120)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=150)
    hebrew_name = models.CharField(max_length=200, blank=True)
    nickname = models.CharField(max_length=150, blank=True)
    birth_date = PartialDateCharField()
    death_date = PartialDateCharField(blank=True)
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
    places = models.ManyToManyField(Place, blank=True, related_name='organizations')
    cover_image = models.ForeignKey(Media, blank=True, null=True)
    start_date = PartialDateCharField()
    end_date = PartialDateCharField(blank=True)

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
    start_date = PartialDateCharField()
    end_date = PartialDateCharField(blank=True)
    place = models.ForeignKey(Place, related_name='events')
    map_context = models.CharField(max_length=20, choices=MAP_CONTEXTS, blank=True)
    people = models.ManyToManyField(Person, blank=True, related_name='events')
    organizations = models.ManyToManyField(Organization, blank=True, related_name='events')
    media = models.ManyToManyField(Media, blank=True, related_name='events')
    project = models.ForeignKey(Project, blank=True, null=True, related_name='events')
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def clean(self):
        if self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({'end_date': 'End date must occur after start date'})


class Annotation(models.Model):
    ANNOTATION_TYPES = (
        ('correspondence', 'Correspondence'),
        ('group', 'Group'),
        ('travel', 'Travel'),
        ('trend', 'Trend')
    )

    ANNOTATION_LINKS = (
        ('path', 'Path'),
        ('correspondence', 'Correspondence'),
        ('flow', 'Flow')
    )

    places = models.ManyToManyField(Place, blank=True, related_name='annotations')
    events = models.ManyToManyField(Event, related_name='annotations')
    type = models.CharField(max_length=20, choices=ANNOTATION_TYPES)
    description = models.TextField(blank=True)
    link_style = models.CharField(max_length=20, choices=ANNOTATION_LINKS)
