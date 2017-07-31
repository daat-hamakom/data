from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

import re
from datetime import datetime
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
from daat.utils import cache_delete_startswith


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
    if instance.type == 'image' and (created or instance.__gen_thumbnails__):
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
    media_titles = []
    for index, row in enumerate(reader_list):
        row_index = index + 2
        if not row.get('Skip Event', None):
            errors = validate_event(row.get('Title', None), row.get('Place VIAF', None), row.get('Time', None))

        if not row.get('Ref. Skip Event', None):
            ref_errors = validate_event(row.get('Ref. Title', None), row.get('Ref. Place VIAF', None), row.get('Ref. Time', None), 'ref ')

        if not row.get('Skip Event', None) or not row.get('Ref. Skip Event', None):
            extra_errors = validate_extra(row, zip_list)
            if row.get('filename1', None):
                title1 = row.get('image-title1', None)
                if title1 not in media_titles:
                    media_titles.append(title1)
                else:
                    extra_errors.append('title1 ' + title1 + ' already mentioned in csv')

            if row.get('filename2', None):
                title2 = row.get('image-title2', None)
                if title2 not in media_titles:
                    media_titles.append(title2)
                else:
                    extra_errors.append('title2 ' + title2 + ' already mentioned in csv')

        if len(errors) or len(ref_errors) or len(extra_errors):
            all_errors = errors + ref_errors + extra_errors
            error = str(row_index) + ' - ' + ', '.join(all_errors)

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
    if instance.deleted:
        delete_import.apply_async(countdown=10,
                                  kwargs={'payload': {'id': instance.id}},
                                  retry_policy={'max_retries': 3, 'interval_step': 30})

    if created or instance.status == 'new':
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

    csv_file = requests.get(import_object.csv).content.decode('utf-8')
    reader_list = csv.DictReader(io.StringIO(csv_file))

    #  todo - create new project
    try:
        try:
            project = Project.objects.get(title=import_object.project)
        except Project.DoesNotExist:
            project = Project(title=import_object.project, creator=creator)
            project.save()

        for row in reader_list:
            #  todo - create media
            if not row.get('Ref. Skip Event', None) or not row.get('Skip Event', None):
                media1 = import_media(row.get('filename1', None), row.get('image-title1', None), row.get('image-source1', None),
                                      import_object.copyrights, import_object.copyrights_source_url, zip_object, creator)

                media2 = import_media(row.get('filename2', None), row.get('image-title2', None), row.get('image-source2', None),
                                      import_object.copyrights, import_object.copyrights_source_url, zip_object, creator)

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

                tags = row.get('Tags', None)

            #  create event
            if not row.get('Skip Event', None):
                event_dict = dict()
                event_dict['creator'] = creator
                event_dict['project'] = project
                event_dict['map_context'] = import_object.map_context
                event_dict['title'] = row.get('Title', None)
                event_dict['description'] = create_description(import_object.description1_subtitle, import_object.description2_subtitle,
                                                               import_object.description3_subtitle, row.get('Description 1', None),
                                                               row.get('Description 2', None), row.get('Description 3', None))

                event_dict['place'] = Place.objects.get(**extract_filter(row.get('Place VIAF', None)))
                event_dict['tags'] = tags.split(',')

                #  parse if
                time = row.get('Time', None)
                event_dict['circa_date'] = 'ca.' in time
                time = time.replace('ca.', '')
                match = re.search(r"^(\d{4})-(\d{4})$", time)

                if match:
                    event_dict['start_date'] = match.group(1) + '-00-00'
                    event_dict['end_date'] = match.group(2) + '-00-00'
                else:
                    match = re.search(r"(\d{4})", time)
                    event_dict['start_date'] = match.group(1) + '-00-00'

                #  todo - link media and persons
                event = Event(**event_dict)
                event.save()

                if person1:
                    event.people.add(person1)

                if person2:
                    event.people.add(person2)

                if media1:
                    event.media.add(media1)
                    event.media_icon = media1
                    event.save()

                if media2:
                    event.media.add(media2)

            #  create event
            if not row.get('Ref. Skip Event', None):
                event_dict = dict()
                event_dict['creator'] = creator
                event_dict['project'] = project
                event_dict['map_context'] = import_object.map_context
                event_dict['title'] = row.get('Ref. Title', None)
                event_dict['description'] = create_description(import_object.description1_subtitle, import_object.description2_subtitle,
                                                               import_object.description3_subtitle, row.get('Description 1', None),
                                                               row.get('Description 2', None), row.get('Description 3', None))

                event_dict['place'] = Place.objects.get(**extract_filter(row.get('Ref. Place VIAF', None)))
                event_dict['tags'] = tags.split(',')

                #  parse if
                time = row.get('Ref. Time', None)
                event_dict['circa_date'] = 'ca.' in time
                time = time.replace('ca.', time)
                match = re.search(r"^(\d{4})-(\d{4})$", time)

                if match:
                    event_dict['start_date'] = match.group(1) + '-00-00'
                    event_dict['end_date'] = match.group(2) + '-00-00'
                else:
                    match = re.search(r"(\d{4})", time)
                    event_dict['start_date'] = match.group(1) + '-00-00'

                #  todo - link media and persons
                ref_event = Event(**event_dict)
                ref_event.save()

                if person1:
                    ref_event.people.add(person1)

                if person2:
                    ref_event.people.add(person2)

                if media1:
                    ref_event.media.add(media1)
                    ref_event.media_icon = media1
                    ref_event.save()

                if media2:
                    ref_event.media.add(media2)

            if not row.get('Ref. Skip Event', None) and not row.get('Skip Event', None):
                #  todo - create annotation
                annotation = Annotation(type='reference', creator=creator, origin=ref_event)
                annotation.save()

                annotation.events.add(event)
                annotation.events.add(ref_event)
                annotation.save()
    except Exception as e:
        import_object.error_log = str(e)
        import_object.status = 'failed'
        import_object.save()
        return

    import_object.status = 'uploaded'
    import_object.save()


@shared_task
def migrate_import(payload):
    import_object = Import.objects.get(pk=payload['id'])
    import_object.status = 'migrating'
    import_object.save()

    try:
        temp_project = Project.objects.get(title=import_object.project)

        events = Event.objects.filter(project=temp_project)
        for event in events:
            event.project = import_object.target_project
            event.save()

        temp_project.delete()
    except Exception as e:
        import_object.error_log = str(e)
        import_object.status = 'failed'
        import_object.save()
        return

    import_object.status = 'migrated'
    import_object.save()
    # clean cache after migration
    cache_delete_startswith('/api/')


@shared_task
def delete_import(payload):
    import_object = Import.objects.get(pk=payload['id'])
    import_object.status = 'deleting'
    import_object.error_log = ''
    import_object.save()

    try:
        temp_project = Project.objects.get(title=import_object.project)

        csv_file = requests.get(import_object.csv).content.decode('utf-8')
        reader_list = csv.DictReader(io.StringIO(csv_file))

        for row in reader_list:
            #  todo - create media
            if row.get('filename1', None):
                try:
                    media1 = Media.objects.get(title=row.get('image-title1', None))

                    #  change name for uniqueness
                    media1.title += ' - ' + datetime.now().strftime("%Y%m%d%H%M%S")
                    media1.save()

                    media1.delete()
                except ObjectDoesNotExist:
                    pass

            if row.get('filename2', None):
                try:
                    media2 = Media.objects.get(title=row.get('image-title2', None))

                    #  change name for uniqueness
                    media2.title += ' - ' + datetime.now().strftime("%Y%m%d%H%M%S")
                    media2.save()

                    media2.delete()
                except ObjectDoesNotExist:
                    pass

            if not row.get('Ref. Skip Event', None) and not row.get('Skip Event', None):
                try:
                    ref_events = Event.objects.filter(project=temp_project, title=row.get('Ref. Title', None))
                    if ref_events.count() == 0:
                        pass

                    annotation = Annotation.objects.filter(origin=ref_events[0])
                    annotation.delete()
                except ObjectDoesNotExist:
                    pass

            if not row.get('Ref. Skip Event', None):
                try:
                    ref_events = Event.objects.filter(project=temp_project, title=row.get('Ref. Title', None))
                    ref_events.delete()
                except ObjectDoesNotExist:
                    pass

            if not row.get('Skip Event', None):
                try:
                    events = Event.objects.filter(project=temp_project, title=row.get('Title', None))
                    events.delete()
                except ObjectDoesNotExist:
                    pass

        temp_project.delete()
    except Exception as e:
        import_object.error_log = str(e)
        import_object.status = 'failed'
        import_object.save()
        return

    import_object.status = 'deleted'
    import_object.save()


def validate_event(title, place_viaf, time, prefix=''):
    errors = []
    # check if title in csv
    if not title:
        errors.append(prefix + 'title is missing')

    # check if place in csv
    if not place_viaf:
        errors.append(prefix + 'place viaf is missing')
    else:
        # check if place exists
        place_count = Place.objects.filter(**extract_filter(place_viaf)).count()
        if place_count < 1:
            errors.append(prefix + 'place viaf is not in db')
        if place_count > 1:
            errors.append(prefix + 'place viaf not unique')

    # check if time in csv
    parsed_time = None
    if not time:
        errors.append(prefix + 'time required')
    else:
        regexes = [r"^(\d{4})$", r"^ca.(\d{4})$", r"^ca.(\d{4})-(\d{4})$", r"^(\d{4})-(\d{4})$"]
        for regex in regexes:
            match = re.search(regex, time)

            if match:
                parsed_time = match.group(1)
                break

        if not parsed_time:
            errors.append(prefix + 'time is not in the right format')

    return errors


def validate_extra(row, zip_list):
    errors = []
    # check person in db if exists
    person1_viaf = row.get('Person 1 VIAF', None)
    if person1_viaf and not row.get('Skip Person 1', None):
        person_count = Person.objects.filter(**extract_filter(person1_viaf)).count()
        if person_count < 1:
            errors.append('person 1 not in db')
        if person_count > 1:
            errors.append('person 1 not unique')

    person2_viaf = row.get('Person 2 VIAF', None)
    if person2_viaf and not row.get('Skip Person 2', None):
        person_count = Person.objects.filter(**extract_filter(person2_viaf)).count()
        if person_count < 1:
            errors.append('person 2 not in db')
        if person_count > 1:
            errors.append('person 2 not unique')

    filename1 = row.get('filename1', None)
    if filename1:
        filename1 += '.jpg'
        if filename1 not in zip_list:
            errors.append('file1 not in zip')
        elif not row.get('image-title1', None):
            errors.append('file 1 missing title')
        else:
            title = row.get('image-title1', None)
            if Media.objects.all_with_deleted().filter(title=title).count() > 0:
                errors.append('file 1 title not unique')

    filename2 = row.get('filename2', None)
    if filename2:
        filename2 += '.jpg'
        if filename2 not in zip_list:
            errors.append('file2 not in zip')
        elif not row.get('image-title2', None):
            errors.append('file 2 missing title')
        else:
            title = row.get('image-title2', None)
            if Media.objects.all_with_deleted().filter(title=title).count() > 0:
                errors.append('file 2 title not unique')

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
    if desc1:
        if desc1_sub:
            description_parts.append('<b>' + desc1_sub + '</b>: ' + desc1 + '.')
        else:
            description_parts.append(desc1 + '.')

    if desc2:
        if desc2_sub:
            description_parts.append('<b>' + desc2_sub + '</b>: ' + desc2 + '.')
        else:
            description_parts.append(desc2 + '.')

    if desc3:
        if desc3_sub:
            description_parts.append('<b>' + desc3_sub + '</b>: ' + desc3 + '.')
        else:
            description_parts.append(desc3 + '.')

    return '<br/>'.join(description_parts)


def import_media(filename, title, source, copyrights, copyright_source, zip_object, creator):
    if not filename:
        return None

    s3conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    bucket = s3conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)

    filename_content = zip_object.read(filename + '.jpg')

    k = Key(bucket)
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    k.key = 'media/{}-{}.jpg'.format(filename, ts)
    k.set_contents_from_string(filename_content)
    k.make_public()
    url = k.generate_url(expires_in=0, query_auth=False)

    media_dict = dict(file=url, creator=creator, title=title, source=source)
    if copyrights:
        media_dict["copyrights"] = copyrights

    if copyrights:
        media_dict["source_url"] = copyright_source

    media = Media(**media_dict)
    media.save()
    return media
