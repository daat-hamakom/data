# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-06-08 13:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0030_import'),
    ]

    operations = [
        migrations.AddField(
            model_name='import',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('uploading', 'uploading'), ('uploaded', 'uploaded'), ('testing', 'testing')], default='new', max_length=20),
        ),
        migrations.AlterField(
            model_name='import',
            name='target_project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='imports', to='maps.Project'),
        ),
    ]
