# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import daat.maps.models
import daat.maps.utils


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0003_auto_20151115_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=daat.maps.models.PartialDateCharField(validators=[daat.maps.utils.partial_date_validator], blank=True, help_text='Date in YYYY-MM-DD format, use 00 to denote month/day ranges', max_length=10),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=daat.maps.models.PartialDateCharField(validators=[daat.maps.utils.partial_date_validator], help_text='Date in YYYY-MM-DD format, use 00 to denote month/day ranges', max_length=10),
        ),
        migrations.AlterField(
            model_name='organization',
            name='end_date',
            field=daat.maps.models.PartialDateCharField(validators=[daat.maps.utils.partial_date_validator], blank=True, help_text='Date in YYYY-MM-DD format, use 00 to denote month/day ranges', max_length=10),
        ),
        migrations.AlterField(
            model_name='organization',
            name='start_date',
            field=daat.maps.models.PartialDateCharField(validators=[daat.maps.utils.partial_date_validator], help_text='Date in YYYY-MM-DD format, use 00 to denote month/day ranges', max_length=10),
        ),
        migrations.AlterField(
            model_name='person',
            name='birth_date',
            field=daat.maps.models.PartialDateCharField(validators=[daat.maps.utils.partial_date_validator], help_text='Date in YYYY-MM-DD format, use 00 to denote month/day ranges', max_length=10),
        ),
        migrations.AlterField(
            model_name='person',
            name='death_date',
            field=daat.maps.models.PartialDateCharField(validators=[daat.maps.utils.partial_date_validator], blank=True, help_text='Date in YYYY-MM-DD format, use 00 to denote month/day ranges', max_length=10),
        ),
        migrations.AlterField(
            model_name='project',
            name='end_date',
            field=daat.maps.models.PartialDateCharField(validators=[daat.maps.utils.partial_date_validator], blank=True, help_text='Date in YYYY-MM-DD format, use 00 to denote month/day ranges', max_length=10),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=daat.maps.models.PartialDateCharField(validators=[daat.maps.utils.partial_date_validator], help_text='Date in YYYY-MM-DD format, use 00 to denote month/day ranges', max_length=10),
        ),
    ]
