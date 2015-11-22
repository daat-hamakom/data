# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='category',
        ),
        migrations.RemoveField(
            model_name='project',
            name='research_field',
        ),
        migrations.AddField(
            model_name='media',
            name='type',
            field=models.CharField(choices=[('image', 'Image'), ('sound', 'Sound'), ('document', 'Document'), ('video', 'Video')], max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='biography',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='synopsis',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='researcher',
            name='biography',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]
