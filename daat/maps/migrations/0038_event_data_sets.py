# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-07-04 14:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0037_auto_20170704_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='data_sets',
            field=models.ManyToManyField(blank=True, related_name='data_sets', to='maps.DataSet'),
        ),
    ]