import re
import os

from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.cache import cache


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


def create_filename(dir):
    def wrapper(filename):
        name = filename.split('.')[0]
        ext = filename.split('.')[-1]
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = '%s-%s.%s' % (name, ts, ext)
        return os.path.join(dir, filename)
    return wrapper


# now cache delete includes subkeys
def cache_delete_startswith(path):
    for key in cache._cache.keys():
        if key.startswith(path):
            del cache.delete[key]
