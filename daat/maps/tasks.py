from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

import re
import io
import csv
import requests
from zipfile import ZipFile
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from io import BytesIO
from PIL import Image
from PIL.ImageOps import fit
from celery import shared_task

from django.conf import settings
from .models import Import, Media, Place, Person, Event, Annotation, Project


def gen_image_thumbnails(media):
    s3conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    bucket = s3conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)

    orig = Image.open(BytesIO(requests.get(media.file).content))

    # create the small 50x50 icon
    tmp = BytesIO()
    thumb = fit(orig, (50, 50), method=Image.BICUBIC)
    thumb.save(tmp, format='jpeg')

    tmp.seek(0)
    k = Key(bucket)
    k.key = 'media_thumbs/{}_{}.jpg'.format(media.filename(), 's')
    k.set_contents_from_file(tmp)
    k.make_public()
    tmp.close()

    # create the medium sized thumbnail
    tmp = BytesIO()
    thumb = fit(orig, (320, 214), method=Image.BICUBIC)
    thumb.save(tmp, format='jpeg')

    tmp.seek(0)
    k = Key(bucket)
    k.key = 'media_thumbs/{}_{}.jpg'.format(media.filename(), 'm')
    k.set_contents_from_file(tmp)
    k.make_public()
    tmp.close()

    # create the large sized thumbnail
    tmp = BytesIO()
    im = orig.copy()
    im.thumbnail((1000, 1000))
    im.save(tmp, format='jpeg')

    tmp.seek(0)
    k = Key(bucket)
    k.key = 'media_thumbs/{}_{}.jpg'.format(media.filename(), 'l')
    k.set_contents_from_file(tmp)
    k.make_public()
    tmp.close()


@receiver(post_save, sender=Media)
def create_media_thumbnails(sender, instance=None, created=False, **kwargs):
    if created and instance.type == 'image':
        gen_image_thumbnails(instance)


@shared_task
def validate_import(payload):
    import_object = Import.objects.get(pk=payload['id'])
    import_object.status = 'testing'
    import_object.save()

    # get zip
    zip_file = requests.get(import_object.media).content
    zip_object = ZipFile(io.BytesIO(zip_file))
    zip_list = [info.filename for info in zip_object.infolist()]

    csv_file = requests.get(import_object.csv).content.decode('utf-8')
    reader_list = csv.DictReader(io.StringIO(csv_file))

    csv_errors = []
    errors = []
    ref_errors = []
    for index, row in enumerate(reader_list):
        row_index = index + 2
        if not row.get('Skip Event', None):
            errors = validate_event(row.get('Title', None), row.get('Place VIAF', None), row.get('Time', None))

        if not row.get('Ref. Skip Event', None):
            ref_errors = validate_event(row.get('Ref. Title', None), row.get('Ref. Place VIAF', None), row.get('Ref. Time', None))

        extra_errors = validate_extra(row, zip_list)

        if len(errors) or len(ref_errors) or len(extra_errors):
            error = str(row_index) + ' - '
            if len(errors):
                error += 'Event Errors: ' + ', '.join(errors) + ' '

            if len(ref_errors):
                error += 'Ref. Event Errors: ' + ', '.join(ref_errors) + ' '

            if len(extra_errors):
                error += 'Extras Errors: ' + ', '.join(extra_errors) + ' '

            csv_errors.append(error)

    if len(csv_errors):
        import_object.status = 'invalid'
        import_object.error_log = '\n'.join(csv_errors)
        import_object.save()
    else:
        import_object.status = 'valid'
        import_object.save()


@receiver(post_save, sender=Import)
def test_import(sender, instance=None, created=False, **kwargs):
    if created:
        print('check errors with celery, and update instance')
        validate_import.apply_async(countdown=10,
                                    kwargs={'payload': {'id': instance.id}},
                                    retry_policy={'max_retries': 3, 'interval_step': 30})


@shared_task
def execute_import(payload):
    import_object = Import.objects.get(pk=payload['id'])
    import_object.status = 'uploading'
    import_object.save()

    # get user
    app_label, model_name = settings.AUTH_USER_MODEL.split('.')
    user_model = apps.get_model(app_label=app_label, model_name=model_name)
    creator = user_model.objects.get(pk=payload['user_id'])

    # get zip
    zip_file = requests.get(import_object.media).content
    zip_object = ZipFile(io.BytesIO(zip_file))
    zip_list = [info.filename for info in zip_object.infolist()]

    csv_file = requests.get(import_object.csv).content.decode('utf-8')
    reader_list = csv.DictReader(io.StringIO(csv_file))

    #  todo - create new project
    try:
        project = Project.objects.get(title=import_object.project)
    except Project.DoesNotExist:
        project = Project(title=import_object.project, creator=creator)
        project.save()

    for row in reader_list:
        #  todo - create media
        media1 = Media()
        media2 = Media()

        #  collect people for later adding to events
        person1_viaf = row.get('Person 1 VIAF', None)
        if person1_viaf and not row.get('Skip Person 1', None):
            person1 = Person.objects.get(**extract_filter(person1_viaf))
        else:
            person1 = None

        person2_viaf = row.get('Person 2 VIAF', None)
        if person2_viaf and not row.get('Skip Person 2', None):
            person2 = Person.objects.get(**extract_filter(person2_viaf))
        else:
            person2 = None

        #  create event
        if not row.get('Skip Event', None):
            event_dict = dict()
            event_dict['creator'] = creator
            event_dict['project'] = project
            event_dict['title'] = row.get('Title', None)
            event_dict['description'] = create_description(import_object.description1_subtitle, import_object.description2_subtitle,
                                                           import_object.description3_subtitle, row.get('Description 1', None),
                                                           row.get('Description 2', None), row.get('Description 3', None))

            event_dict['place'] = Place.objects.get(**extract_filter(row.get('Place VIAF', None)))

            #  parse if
            time = row.get('Time', None)
            event_dict['circa_date'] = 'ca.' in time
            time = time.replace('ca. ', time)
            match = re.search(r"(\d{4}) - (\d{4})", time)

            if match:
                event_dict['start_date'] = match.group(1)
                event_dict['end_date'] = match.group(2)
            else:
                match = re.search(r"(\d{4})", time)
                event_dict['start_date'] = match.group(1)

            #  todo - link media and persons
            event = Event(**event_dict)
            event.save()

            if person1:
                event.people.add(person1)

            if person2:
                event.people.add(person2)

        #  create event
        if not row.get('Ref. Skip Event', None):
            event_dict = dict()
            event_dict['creator'] = creator
            event_dict['project'] = project
            event_dict['title'] = row.get('Ref. Title', None)
            event_dict['description'] = create_description(import_object.description1_subtitle, import_object.description2_subtitle,
                                                           import_object.description3_subtitle, row.get('Description 1', None),
                                                           row.get('Description 2', None), row.get('Description 3', None))

            event_dict['place'] = Place.objects.get(**extract_filter(row.get('Ref. Place VIAF', None)))

            #  parse if
            time = row.get('Ref. Time', None)
            event_dict['circa_date'] = 'ca.' in time
            time = time.replace('ca. ', time)
            match = re.search(r"(\d{4}) - (\d{4})", time)

            if match:
                event_dict['start_date'] = match.group(1)
                event_dict['end_date'] = match.group(2)
            else:
                match = re.search(r"(\d{4})", time)
                event_dict['start_date'] = match.group(1)

            #  todo - link media and persons
            ref_event = Event(**event_dict)
            ref_event.save()

            if person1:
                ref_event.people.add(person1)

            if person2:
                ref_event.people.add(person2)

        if event and ref_event:
            #  todo - create annotation
            annotation = Annotation(type='group', creator=creator)
            annotation.save()

            annotation.events.add(event)
            annotation.events.add(ref_event)
            annotation.save()

    import_object.status = 'uploaded'
    import_object.save()


@shared_task
def migrate_import(payload):
    import_object = Import.objects.get(pk=payload['id'])
    import_object.status = 'migrating'
    import_object.save()

    temp_project = Project.objects.get(title=import_object.project)

    events = Event.objects.filter(project=temp_project)
    for event in events:
        event.project = import_object.target_project
        event.save()

    temp_project.delete()

    import_object.status = 'migrated'
    import_object.save()


@shared_task
def delete_import(payload):
    import_object = Import.objects.get(pk=payload['id'])
    import_object.status = 'deleting'
    import_object.save()

    import_object.status = 'deleted'
    import_object.save()


def validate_event(title, place_viaf, time):
    errors = []
    # check if title in csv
    if not title:
        errors.append('title is missing')

    # check if place in csv
    if not place_viaf:
        errors.append('place viaf is missing')

    # check if place exists
    place_count = Place.objects.filter(**extract_filter(place_viaf)).count()
    if place_count != 1:
        errors.append('place viaf is not in db')

    # check if time in csv
    parsed_time = None
    if not time:
        errors.append('time is missing')
    else:
        regexes = [r"(\d{4})", r"ca. (\d{4})", r"ca. (\d{4}) - (\d{4})", r"(\d{4}) - (\d{4})"]
        for regex in regexes:
            match = re.search(regex, time)

            if match:
                parsed_time = match.group(1)
                break

        if not parsed_time:
            errors.append('time is not in the right format')

    return errors


def validate_extra(row, zip_list):
    errors = []
    # check person in db if exists
    person1_viaf = row.get('Person 1 VIAF', None)
    if person1_viaf and not row.get('Skip Person 1', None):
        person_count = Person.objects.filter(**extract_filter(person1_viaf)).count()
        if person_count != 1:
            errors.append('person 1 not in db')

    person2_viaf = row.get('Person 2 VIAF', None)
    if person2_viaf and not row.get('Skip Person 2', None):
        person_count = Person.objects.filter(**extract_filter(person2_viaf)).count()
        if person_count != 1:
            errors.append('person 2 not in db')

    filename1 = row.get('filename1', None)
    if filename1:
        filename1 += '.jpg'
        if filename1 not in zip_list:
            errors.append('file1 not in zip')
        elif not row.get('image-title1', None):
            errors.append('file 1 missing title')

    filename2 = row.get('filename2', None)
    if filename2:
        filename2 += '.jpg'
        if filename2 not in zip_list:
            errors.append('file1 not in zip')
        elif not row.get('image-title2', None):
            errors.append('file 1 missing title')

    return errors


def extract_filter(str):
    if '#' in str:
        index = str.replace('#', '')
        return {"id": index}
    else:
        return {"viaf_id": str}


def create_description(desc1_sub, desc2_sub, desc3_sub,
                       desc1, desc2, desc3):
    description_parts = []
    if desc1 and desc1_sub:
        description_parts.append(desc1_sub + ': ' + desc1)

    if desc2 and desc2_sub:
        description_parts.append(desc2_sub + ': ' + desc2)

    if desc3 and desc3_sub:
        description_parts.append(desc3_sub + ': ' + desc3)

    return '\n'.join(description_parts)
