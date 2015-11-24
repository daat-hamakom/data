# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0004_remove_project_institution'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='url',
            field=models.CharField(help_text='If file not uploaded, a URL must be filled (e.g. Youtube video, external link...)', max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='file',
            field=s3direct.fields.S3DirectField(blank=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='type',
            field=models.CharField(max_length=20, blank=True, choices=[('image', 'Image'), ('sound', 'Sound'), ('document', 'Document'), ('video', 'Video'), ('link', 'Link')]),
        ),
        migrations.AlterField(
            model_name='place',
            name='alt_name',
            field=django.contrib.postgres.fields.ArrayField(null=True, base_field=models.CharField(max_length=300), help_text='Multiple alternative names allowed, press Enter between entires', blank=True, size=None),
        ),
    ]
