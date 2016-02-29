import requests

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.conf import settings
from io import BytesIO
from PIL import Image
from PIL.ImageOps import fit

def gen_image_thumbnails(media):
    s3conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    bucket = s3conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)

    orig = Image.open(BytesIO(requests.get(media.file).content))

    for name, size in {'s': (40, 40), 'm': (320, 214)}.items():
        tmp = BytesIO()
        thumb = fit(orig, size, method=Image.BICUBIC)
        thumb.save(tmp, format='jpeg')

        tmp.seek(0)
        k = Key(bucket)
        k.key = 'media_thumbs/{}_{}.jpg'.format(media.filename(), name)
        k.set_contents_from_file(tmp)
        k.make_public()
        tmp.close()
