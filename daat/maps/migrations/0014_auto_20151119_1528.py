# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0013_auto_20151119_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='alt_name',
            field=django.contrib.postgres.fields.ArrayField(help_text='Single alt name with no commas, or comma-separated list of names (e.g. <code>Tel-Aviv,Tel Aviv,תל אביב)</code>', base_field=models.CharField(max_length=300), blank=True, null=True, size=None),
        ),
    ]
