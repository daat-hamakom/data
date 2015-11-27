# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0005_auto_20151124_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='subtitle',
            field=models.CharField(blank=True, max_length=160),
        ),
        migrations.AlterField(
            model_name='place',
            name='alt_name',
            field=django.contrib.postgres.fields.ArrayField(size=None, base_field=models.CharField(max_length=300), blank=True, help_text='Single alt name with no commas, or comma-separated list of names (e.g. <code>Tel-Aviv,Tel Aviv,תל אביב)</code>', null=True),
        ),
    ]
