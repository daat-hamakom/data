# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0015_auto_20151119_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
