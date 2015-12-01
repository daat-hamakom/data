# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0006_auto_20151127_1634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='hebrew_name',
        ),
        migrations.RemoveField(
            model_name='person',
            name='nickname',
        ),
        migrations.AddField(
            model_name='person',
            name='alt_name',
            field=django.contrib.postgres.fields.ArrayField(null=True, size=None, base_field=models.CharField(max_length=300), blank=True, help_text='Single alt name with no commas, or comma-separated list of names (e.g. <code>Shai Agnon,S. Y. Agnon,ש״י עגנון)</code>'),
        ),
    ]
