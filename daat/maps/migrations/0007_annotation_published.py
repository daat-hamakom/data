# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0006_auto_20151115_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
