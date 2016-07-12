# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-12 15:06
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0019_event_circa_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=300), blank=True, help_text='Multiple alternative names allowed, press Enter between entries', null=True, size=None),
        ),
    ]
