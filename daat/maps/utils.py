import math
import re
import requests

from datetime import datetime
from django.core.exceptions import ValidationError
from io import BytesIO
from PIL import Image, ImageOps

def partial_date_validator(s):
    if not re.match(r'^\d\d\d\d-\d\d-\d\d$', s):
        raise ValidationError('Date must be in format YYYY-MM-DD, use 00 for unknowns')
    y, m, d = map(int, s.split('-'))
    if y > 3000:
        raise ValidationError('Invalid year {}'.format(y))
    if m > 12:
        raise ValidationError('Invalid month {}'.format(m))
    if d > 0:
        try:
            dt = datetime.strptime(s, '%Y-%m-%d')
        except ValueError:
            raise ValidationError('Invalid date {}'.format(s))


class SpriteCreator(object):
    def __init__(self, events=None):
        self.events = events or []
        self.json = {}
        self.png = None
        self.basesize = 40

    def build(self):
        size = math.ceil(math.sqrt(len(self.events)))
        sprite_img = Image.new('RGB', (size*self.basesize, size*self.basesize), '#000000')
        blank = Image.new('RGB', (self.basesize, self.basesize), '#ff33aa')
        sprite_img.paste(blank, (0, 0))
        im_count = 1

        for event in self.events:
            if event.icon and (event.icon.file.endswith('jpg') or event.icon.file.endswith('png')):
                print(event.title, event.icon.file)
                try:
                    res = requests.get(event.icon.file)
                    im = Image.open(BytesIO(res.content))
                    thumb = ImageOps.fit(im, (self.basesize, self.basesize))
                    x, y = self.basesize * (im_count % 15), self.basesize * math.floor(im_count / 15)
                    sprite_img.paste(thumb, (x, y))
                    im_count += 1
                except OSError:
                    print('error')
                    x, y = 0, 0
            else:
                print('blank', event.title)
                x, y = 0, 0

            self.json[event.id] = {
                'width': self.basesize,
                'height': self.basesize,
                'x': x,
                'y': y,
                'pixelRatio': 1
            }

            sprite_img.save('out.png')

    def get_json(self):
        pass

    def get_png(self):
        pass
