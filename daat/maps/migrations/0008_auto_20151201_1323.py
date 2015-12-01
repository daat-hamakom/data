# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0007_auto_20151201_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='political_entity',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='type',
            field=models.CharField(max_length=20, choices=[('correspondence', 'Correspondence'), ('group', 'Group'), ('travel', 'Travel'), ('trend', 'Trend'), ('reference', 'Reference'), ('origin', 'Origin'), ('quote', 'Quote')]),
        ),
    ]
