# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0005_auto_20151115_1337'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='media',
            options={'verbose_name_plural': 'media'},
        ),
        migrations.AlterField(
            model_name='media',
            name='file',
            field=s3direct.fields.S3DirectField(),
        ),
    ]
