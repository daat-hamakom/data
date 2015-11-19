# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0011_place_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='area',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True, help_text='Paste any custom <a href="http://geojson.io">GeoJSON</a> here', blank=True),
        ),
    ]
