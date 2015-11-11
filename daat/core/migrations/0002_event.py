# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import daat.core.utils


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=160)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.CharField(validators=[daat.core.utils.partial_date_validator], max_length=10)),
                ('end_date', models.CharField(blank=True, validators=[daat.core.utils.partial_date_validator], max_length=10)),
            ],
        ),
    ]
