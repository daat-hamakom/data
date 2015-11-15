# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0002_auto_20151111_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='project',
            field=models.ForeignKey(to='maps.Project', blank=True, related_name='events', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='person',
            name='hebrew_name',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='researchers',
            field=models.ManyToManyField(to='maps.Researcher', blank=True, related_name='projects'),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='places',
            field=models.ManyToManyField(to='maps.Place', blank=True, related_name='annotations'),
        ),
        migrations.AlterField(
            model_name='event',
            name='organizations',
            field=models.ManyToManyField(to='maps.Organization', blank=True, related_name='events'),
        ),
        migrations.AlterField(
            model_name='event',
            name='people',
            field=models.ManyToManyField(to='maps.Person', blank=True, related_name='events'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='places',
            field=models.ManyToManyField(to='maps.Place', blank=True, related_name='organizations'),
        ),
    ]
