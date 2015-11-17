# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0007_annotation_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='institution',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='subtitle',
            field=models.CharField(max_length=150, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='supported_by',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='researcher',
            name='affiliation',
            field=models.CharField(max_length=150, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='project',
            field=models.ForeignKey(to='maps.Project', related_name='events', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='media',
            name='copyrights',
            field=models.CharField(help_text='For no copyrights use "Public Domain"', max_length=200),
        ),
    ]
