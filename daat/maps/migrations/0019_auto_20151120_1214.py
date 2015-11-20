# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('maps', '0018_auto_20151120_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='creator',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='creator',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='media',
            name='creator',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organization',
            name='creator',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='creator',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='place',
            name='creator',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='creator',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
    ]
