# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import daat.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='file',
            field=models.FileField(upload_to=daat.core.models.concat_category),
        ),
    ]
