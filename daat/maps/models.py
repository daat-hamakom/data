from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.postgres.fields import ArrayField, HStoreField
from django.core.exceptions import ValidationError
from django.db import models
from geoposition.fields import GeopositionField
from s3direct.fields import S3DirectField
from safedelete.models import safedelete_mixin_factory, DELETED_VISIBLE_BY_PK, SOFT_DELETE

from .utils import partial_date_validator


SafeDeleteMixin = safedelete_mixin_factory(policy=SOFT_DELETE, visibility=DELETED_VISIBLE_BY_PK)

def concat_category(i, f):
    return '{}/{}'.format(i.category, f)


class PartialDateCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        kwargs['validators'] = [partial_date_validator]
        kwargs['help_text'] = 'Date in YYYY-MM-DD format, use 00 to denote month/day ranges'
        return super().__init__(*args, **kwargs)


class CreatorPermissionsMixin(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)

    class Meta:
        abstract = True


class Media(CreatorPermissionsMixin, SafeDeleteMixin):

    FILETYPES = (
        ('image', 'Image'),
        ('sound', 'Sound'),
        ('document', 'Document'),
        ('video', 'Video'),
    )

    file = S3DirectField(dest='media')
    type = models.CharField(max_length=20, choices=FILETYPES, blank=True)
    title = models.CharField(max_length=120)
    source = models.CharField(max_length=200, blank=True)
    source_url = models.CharField(max_length=500, blank=True)
    copyrights = models.CharField(max_length=200, help_text='For no copyrights use "Public Domain"')

    class Meta:
        verbose_name_plural = 'media'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        FILE_MAPPINGS = {
            'image': ['jpg', 'png', 'gif'],
            'sound': ['mp3', 'wav'],
            'document': ['pdf', 'txt'],
            'video': ['mp4', 'avi', 'mov']
        }
        extension = self.file.split('.')[-1].lower()
        extensions = dict((v, k) for k in FILE_MAPPINGS for v in FILE_MAPPINGS[k])
        try:
            self.type = extensions[extension]
        except:
            pass
        super().save(*args, **kwargs)


class Researcher(CreatorPermissionsMixin, SafeDeleteMixin):
    title = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=150)
    affiliation = models.CharField(max_length=150, blank=True)
    biography = RichTextField(blank=True)
    profile_image = models.FileField(upload_to='researcher_profiles', blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Project(CreatorPermissionsMixin, SafeDeleteMixin):
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=150, blank=True)
    institution = models.CharField(max_length=200, blank=True)
    supported_by = models.CharField(max_length=200, blank=True)
    researchers = models.ManyToManyField(Researcher, blank=True, related_name='projects')
    synopsis = RichTextField(blank=True)
    cover_image = models.ForeignKey(Media, blank=True, null=True)
    start_date = PartialDateCharField()
    end_date = PartialDateCharField(blank=True)

    def __str__(self):
        return self.title

    def clean(self):
        if self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({'end_date': 'End date must occur after start date'})


class Place(CreatorPermissionsMixin, SafeDeleteMixin):
    name = models.CharField(max_length=200)
    alt_name = ArrayField(models.CharField(max_length=300), blank=True, null=True,
        help_text='Single alt name with no commas, or comma-separated list of names' +
        ' (e.g. <code>Tel-Aviv,Tel Aviv,תל אביב)</code>')
    position = GeopositionField()
    area = HStoreField(blank=True, null=True, help_text='Paste any custom <a href="http://geojson.io">GeoJSON</a> here')

    def __str__(self):
        return self.name


class Person(CreatorPermissionsMixin, SafeDeleteMixin):
    title = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=120)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=150)
    hebrew_name = models.CharField(max_length=200, blank=True)
    nickname = models.CharField(max_length=150, blank=True)
    birth_date = PartialDateCharField()
    death_date = PartialDateCharField(blank=True)
    biography = RichTextField(blank=True)
    profile_image = models.ForeignKey(Media, blank=True, null=True)
    places = models.ManyToManyField(Place, blank=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def clean(self):
        if self.death_date:
            if self.death_date < self.birth_date:
                raise ValidationError({'death_date': 'Death date must occur after birth date'})


class Organization(CreatorPermissionsMixin, SafeDeleteMixin):
    name = models.CharField(max_length=150)
    alt_name = models.CharField(max_length=150, blank=True)
    description = RichTextField(blank=True)
    type = models.CharField(max_length=200, blank=True)
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


class Event(CreatorPermissionsMixin, SafeDeleteMixin):
    MAP_CONTEXTS = (
        ('neighbourhood', 'Neighbourhood'),
        ('city', 'City'),
        ('province', 'Province'),
        ('country', 'Country'),
        ('continent', 'Continent'),
        ('world', 'World'),
    )

    published = models.BooleanField(default=False)
    title = models.CharField(max_length=160)
    description = RichTextField(blank=True)
    start_date = PartialDateCharField()
    end_date = PartialDateCharField(blank=True)
    place = models.ForeignKey(Place, related_name='events')
    map_context = models.CharField(max_length=20, choices=MAP_CONTEXTS, blank=True)
    people = models.ManyToManyField(Person, blank=True, related_name='events')
    organizations = models.ManyToManyField(Organization, blank=True, related_name='events')
    media = models.ManyToManyField(Media, blank=True, related_name='events')
    project = models.ForeignKey(Project, related_name='events')
    next_event = models.ForeignKey('Event', blank=True, null=True)


    def __str__(self):
        return self.title

    def clean(self):
        if self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({'end_date': 'End date must occur after start date'})


class Annotation(CreatorPermissionsMixin, SafeDeleteMixin):
    ANNOTATION_TYPES = (
        ('correspondence', 'Correspondence'),
        ('group', 'Group'),
        ('travel', 'Travel'),
        ('trend', 'Trend'),
        ('reference', 'Reference'),
        ('origin', 'Origin'),
    )

    ANNOTATION_LINKS = (
        ('path', 'Path'),
        ('correspondence', 'Correspondence'),
        ('flow', 'Flow'),
    )

    places = models.ManyToManyField(Place, blank=True, related_name='annotations')
    events = models.ManyToManyField(Event, related_name='annotations')
    type = models.CharField(max_length=20, choices=ANNOTATION_TYPES)
    description = RichTextField(blank=True)
    origin = models.ForeignKey(Place, blank=True, null=True)
    link_style = models.CharField(max_length=20, choices=ANNOTATION_LINKS)
    published = models.BooleanField(default=False)

    def __str__(self):
        evs = map(str, self.events.all())
        return '({})'.format(', '.join(evs))
