# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.postgres.operations import HStoreExtension
from django.db import migrations, models
import django.contrib.postgres.fields.hstore



class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0010_event_next_event'),
    ]

    operations = [
        HStoreExtension(),
        migrations.AddField(
            model_name='place',
            name='area',
            field=django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True),
        ),
    ]
