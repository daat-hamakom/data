# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 09:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0016_auto_20160515_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='title',
            field=models.CharField(blank=True, help_text='Group title (leave empty for all other annotation types)', max_length=160),
        ),
        migrations.AddField(
            model_name='place',
            name='zoomlevel',
            field=models.CharField(choices=[('area', 'Area'), ('metropolis', 'Metropolis'), ('largecity', 'Large City'), ('city', 'City'), ('town', 'Town'), ('site', 'Site')], default='city', max_length=20),
        ),
    ]