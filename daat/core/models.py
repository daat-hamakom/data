from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from .utils import partial_date_validator


class DaatUser(AbstractUser):
    pass


class Event(models.Model):
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    start_date = models.CharField(max_length=10, validators=[partial_date_validator])
    end_date = models.CharField(max_length=10, blank=True, validators=[partial_date_validator])

    def __str__(self):
        return self.title

    def clean(self):
        if self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({'end_date': 'End date must occur after start date'})
