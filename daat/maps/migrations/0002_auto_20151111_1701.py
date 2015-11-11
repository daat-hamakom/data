# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='alt_name',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='place',
            name='name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='place',
            name='position',
            field=geoposition.fields.GeopositionField(default='9,9', max_length=42),
            preserve_default=False,
        ),
    ]
