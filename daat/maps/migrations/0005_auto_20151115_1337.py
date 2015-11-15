# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0004_auto_20151115_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='media',
            field=models.ManyToManyField(to='maps.Media', related_name='events', blank=True),
        ),
    ]
