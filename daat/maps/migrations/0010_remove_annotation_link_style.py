# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-05 20:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0009_auto_20151202_0958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annotation',
            name='link_style',
        ),
    ]
