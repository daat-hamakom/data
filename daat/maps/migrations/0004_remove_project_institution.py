# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0003_auto_20151122_1314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='institution',
        ),
    ]
