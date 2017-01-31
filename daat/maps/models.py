from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

from geoposition.fields import GeopositionField
from s3direct.fields import S3DirectField
from safedelete.models import safedelete_mixin_factory, DELETED_VISIBLE_BY_PK, SOFT_DELETE

from .tasks import gen_image_thumbnails
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
        ('link', 'Link')
    )

    file = S3DirectField(dest='media', blank=True)
    url = models.CharField(max_length=500, blank=True, help_text='If file not uploaded, a URL must be filled (e.g. Youtube video, external link...)')
    type = models.CharField(max_length=20, choices=FILETYPES, blank=True)
    title = models.CharField(max_length=200, unique=True)
    source = models.CharField(max_length=200, blank=True)
    source_url = models.CharField(max_length=500, blank=True)
    copyrights = models.CharField(max_length=200, help_text='For no copyrights use "Public Domain"')

    class Meta:
        verbose_name_plural = 'media'
        ordering = ['title']

    def __str__(self):
        return self.title

    def filename(self):
        return self.file.split('/')[-1]

    def clean(self):
        if not self.file and not self.url:
            raise ValidationError({
                'file': 'Either file must be uploaded or URL field must not be blank',
                'url': 'Either file must be uploaded or URL field must not be blank',
            })
        if self.file and self.url:
            raise ValidationError({
                'url': 'URL field cannot be filled out if a file was already uploaded, it must be blank',
            })

    def save(self, *args, **kwargs):
        FILE_MAPPINGS = {
            'image': ['jpg', 'png', 'gif'],
            'sound': ['mp3', 'wav'],
            'document': ['pdf', 'txt'],
            'video': ['mp4', 'avi', 'mov']
        }
        if self.file:
            extension = self.file.split('.')[-1].lower()
            extensions = dict((v, k) for k in FILE_MAPPINGS for v in FILE_MAPPINGS[k])
            try:
                self.type = extensions[extension]
            except:
                pass
        elif self.url:
            self.type = 'link'
        super().save(*args, **kwargs)


@receiver(post_save, sender=Media)
def create_media_thumbnails(sender, instance=None, created=False, **kwargs):
    if created and instance.type == 'image':
        gen_image_thumbnails(instance)


class Researcher(CreatorPermissionsMixin, SafeDeleteMixin):
    title = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=150)
    affiliation = models.CharField(max_length=150, blank=True)
    biography = RichTextField(blank=True)
    profile_image = models.FileField(upload_to='researcher_profiles', blank=True, null=True)

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def name(self):
        return self.__str__()


class Project(CreatorPermissionsMixin, SafeDeleteMixin):
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=150, blank=True)
    supported_by = models.CharField(max_length=200, blank=True)
    researchers = models.ManyToManyField(Researcher, blank=True, related_name='projects')
    synopsis = RichTextField(blank=True)
    cover_image = models.ForeignKey(Media, blank=True, null=True)
    start_date = PartialDateCharField()
    end_date = PartialDateCharField(blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def clean(self):
        if self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({'end_date': 'End date must occur after start date'})


@receiver(post_save, sender=Project)
def clear_project_cache(sender, instance=None, created=False, **kwargs):
    cache.delete('/api/projects/')


class Place(CreatorPermissionsMixin, SafeDeleteMixin):

    ZOOMLEVELS = (
        ('area', 'Area'),
        ('metropolis', 'Metropolis'),
        ('largecity', 'Large City'),
        ('city', 'City'),
        ('town', 'Town'),
        ('site', 'Site'),
    )

    name = models.CharField(max_length=200)
    alt_name = ArrayField(models.CharField(max_length=300), blank=True, null=True,
        help_text='Multiple alternative names allowed, press Enter between entries')
    position = GeopositionField()
    zoomlevel = models.CharField(max_length=20, choices=ZOOMLEVELS, default='city', verbose_name='Zoom level')
    area = JSONField(blank=True, null=True, help_text='Paste any custom <a href="http://geojson.io">GeoJSON</a> here')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


@receiver(post_save, sender=Place)
def clear_place_cache(sender, instance=None, created=False, **kwargs):
    cache.delete('/api/places/')


class Person(CreatorPermissionsMixin, SafeDeleteMixin):
    title = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=120)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=150)
    alt_name = ArrayField(models.CharField(max_length=300), blank=True, null=True,
        help_text='Multiple alternative names allowed, press Enter between entries')
    birth_date = PartialDateCharField()
    death_date = PartialDateCharField(blank=True)
    biography = RichTextField(blank=True)
    profile_image = models.ForeignKey(Media, blank=True, null=True)
    places = models.ManyToManyField(Place, blank=True)

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def clean(self):
        if self.death_date:
            if self.death_date < self.birth_date:
                raise ValidationError({'death_date': 'Death date must occur after birth date'})


@receiver(post_save, sender=Person)
def clear_person_cache(sender, instance=None, created=False, **kwargs):
    cache.delete('/api/people/')


class Organization(CreatorPermissionsMixin, SafeDeleteMixin):
    name = models.CharField(max_length=150)
    alt_name = models.CharField(max_length=150, blank=True)
    description = RichTextField(blank=True)
    type = models.CharField(max_length=200, blank=True)
    places = models.ManyToManyField(Place, blank=True, related_name='organizations')
    cover_image = models.ForeignKey(Media, blank=True, null=True)
    start_date = PartialDateCharField()
    end_date = PartialDateCharField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def clean(self):
        if self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({'end_date': 'End date must occur after start date'})


@receiver(post_save, sender=Organization)
def clear_organization_cache(sender, instance=None, created=False, **kwargs):
    cache.delete('/api/organizations/')


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
    subtitle = models.CharField(max_length=160, blank=True)
    description = RichTextField(blank=True)
    start_date = PartialDateCharField()
    end_date = PartialDateCharField(blank=True)
    circa_date = models.BooleanField(default=False)
    place = models.ForeignKey(Place, related_name='events')
    political_entity = models.CharField(max_length=200, blank=True)
    map_context = models.CharField(max_length=20, choices=MAP_CONTEXTS, blank=True)
    people = models.ManyToManyField(Person, blank=True, related_name='events')
    organizations = models.ManyToManyField(Organization, blank=True, related_name='events')
    tags = ArrayField(models.CharField(max_length=300), blank=True, null=True,
        help_text='Multiple tags allowed, press Enter between entries')
    media = models.ManyToManyField(Media, blank=True, related_name='events')
    media_icon = models.ForeignKey(Media, blank=True, null=True, related_name='events_as_icon')
    project = models.ForeignKey(Project, related_name='events')
    next_event = models.ForeignKey('Event', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.title

    def clean(self):
        if self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({'end_date': 'End date must occur after start date'})

    @property
    def icon(self):
        first_media = self.media.filter(type='image').first()
        if first_media:
            return first_media.file

        person = self.people.first()
        if person:
            person_media = person.profile_image
            if person_media:
                return person_media.file

        return self.project.cover_image.file


@receiver(post_save, sender=Event)
def clear_event_cache(sender, instance=None, created=False, **kwargs):
    cache.delete('/api/events/')


class Annotation(CreatorPermissionsMixin, SafeDeleteMixin):
    ANNOTATION_TYPES = (
        ('group', 'Group'),
        ('reference', 'Reference'),
        ('communication', 'Communication'),
        ('path', 'Path')
    )

    places = models.ManyToManyField(Place, blank=True, related_name='annotations')
    events = models.ManyToManyField(Event, related_name='annotations')
    type = models.CharField(max_length=20, choices=ANNOTATION_TYPES)
    title = models.CharField(max_length=160, blank=True, help_text='Group title (leave empty for all other annotation types)')
    description = RichTextField(blank=True)
    origin = models.ForeignKey(Event, blank=True, null=True)
    media = models.ManyToManyField(Media, blank=True, related_name='annotations')
    published = models.BooleanField(default=False)

    def __str__(self):
        evs = map(str, self.events.all())
        return '({})'.format(', '.join(evs))

    def all_events(self):
        return str(self)


@receiver(post_save, sender=Annotation)
def clear_annotation_cache(sender, instance=None, created=False, **kwargs):
    cache.delete('/api/annotations/')
