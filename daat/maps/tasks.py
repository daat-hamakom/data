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
    im = orig.copy()
    im.thumbnail(320, 214)
    im.save(tmp, format='jpeg')

    tmp.seek(0)
    k = Key(bucket)
    k.key = 'media_thumbs/{}_{}.jpg'.format(media.filename(), 'm')
    k.set_contents_from_file(tmp)
    k.make_public()
    tmp.close()

    # create the large sized thumbnail
    tmp = BytesIO()
    im = orig.copy()
    im.thumbnail(1000, 1000)
    im.save(tmp, format='jpeg')

    tmp.seek(0)
    k = Key(bucket)
    k.key = 'media_thumbs/{}_{}.jpg'.format(media.filename(), 'l')
    k.set_contents_from_file(tmp)
    k.make_public()
    tmp.close()
