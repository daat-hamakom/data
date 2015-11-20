# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0017_researcher_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researcher',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False),
        ),
    ]
