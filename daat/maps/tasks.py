from django.db.models.signals import post_save
from django.dispatch import receiver

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
from .models import Import, Media, Place, Person


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
def import_events(payload):
    import_object = Import.objects.get(pk=payload['id'])
    import_object.status = 'testing'
    import_object.save()

    # todo - get zip
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
            errors = validate_event(row.get('Title', None), row.get('Place VIAF', None), row.get('Front Time', None))

        if not row.get('Skip Ref. Event', None):
            ref_errors = validate_event(row.get('Ref. Title', None), row.get('Ref. Place VIAF', None), row.get('Production Ref. Time', None))

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

    s3conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    bucket = s3conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)


@receiver(post_save, sender=Import)
def test_import(sender, instance=None, created=False, **kwargs):
    if created:
        print('check errors with celery, and update instance')
        import_events.apply_async(countdown=10,
                                  kwargs={'payload': {'id': instance.id}},
                                  retry_policy={'max_retries': 3, 'interval_step': 30})


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
    if person1_viaf:
        person_count = Person.objects.filter(**extract_filter(person1_viaf)).count()
        if person_count != 1:
            errors.append('person 1 not in db')

    person2_viaf = row.get('Person 2 VIAF', None)
    if person2_viaf:
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
