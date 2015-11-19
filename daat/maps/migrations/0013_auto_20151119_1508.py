# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0012_auto_20151119_1438'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='alt_name',
        ),
        migrations.AddField(
            model_name='place',
            name='alt_name',
            field=django.contrib.postgres.fields.ArrayField(null=True, blank=True, base_field=models.CharField(max_length=300), size=None),
        ),
    ]
