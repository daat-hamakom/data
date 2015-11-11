# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20151111_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=20, choices=[('correspondence', 'Correspondence'), ('group', 'Group'), ('travel', 'Travel'), ('trend', 'Trend')])),
                ('description', models.TextField(blank=True)),
                ('link_style', models.CharField(max_length=20, choices=[('path', 'Path'), ('correspondence', 'Correspondence'), ('flow', 'Flow')])),
                ('events', models.ManyToManyField(to='core.Event', related_name='annotations')),
                ('places', models.ManyToManyField(to='core.Place', related_name='annotations')),
            ],
        ),
    ]
