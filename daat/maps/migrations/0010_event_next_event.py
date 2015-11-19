# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0009_auto_20151119_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='next_event',
            field=models.ForeignKey(null=True, to='maps.Event', blank=True),
        ),
    ]
