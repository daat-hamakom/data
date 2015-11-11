from django.db import models
from django.contrib.auth.models import AbstractUser

from .utils import partial_date_validator


class DaatUser(AbstractUser):
    pass


class Event(models.Model):
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    start_date = models.CharField(max_length=10, validators=[partial_date_validator])
    end_date = models.CharField(max_length=10, blank=True, validators=[partial_date_validator])
