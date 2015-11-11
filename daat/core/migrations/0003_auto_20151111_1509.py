# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20151111_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='researcher',
            name='biography',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='researcher',
            name='profile_image',
            field=models.FileField(upload_to='researcher_profiles', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='researcher',
            name='title',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
