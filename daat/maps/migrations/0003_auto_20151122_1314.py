# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0002_auto_20151122_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='origin',
            field=models.ForeignKey(to='maps.Event', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='type',
            field=models.CharField(max_length=20, choices=[('correspondence', 'Correspondence'), ('group', 'Group'), ('travel', 'Travel'), ('trend', 'Trend'), ('reference', 'Reference'), ('origin', 'Origin')]),
        ),
        migrations.AlterField(
            model_name='media',
            name='title',
            field=models.CharField(unique=True, max_length=200),
        ),
    ]
