# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0008_auto_20151117_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='origin',
            field=models.ForeignKey(to='maps.Place', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='type',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='places',
            field=models.ManyToManyField(to='maps.Place', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='research_field',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='type',
            field=models.CharField(choices=[('correspondence', 'Correspondence'), ('group', 'Group'), ('travel', 'Travel'), ('trend', 'Trend'), ('reference', 'Reference')], max_length=20),
        ),
    ]
