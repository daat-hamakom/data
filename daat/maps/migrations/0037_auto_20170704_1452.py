# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-07-04 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0036_dataset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='url',
            field=models.CharField(help_text='Without / and http://, example: draft.daat-hamakum.com', max_length=160),
        ),
    ]
