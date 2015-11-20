# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
import geoposition.fields
import daat.maps.models
import django.contrib.postgres.fields.hstore
from django.contrib.postgres.operations import HStoreExtension
from django.conf import settings
import ckeditor.fields
import s3direct.fields
import daat.maps.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        HStoreExtension(),
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('deleted', models.BooleanField(default=False)),
                ('type', models.CharField(max_length=20, choices=[('correspondence', 'Correspondence'), ('group', 'Group'), ('travel', 'Travel'), ('trend', 'Trend'), ('reference', 'Reference')])),
                ('description', models.TextField(blank=True)),
                ('link_style', models.CharField(max_length=20, choices=[('path', 'Path'), ('correspondence', 'Correspondence'), ('flow', 'Flow')])),
                ('published', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('deleted', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=160)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('start_date', daat.maps.models.PartialDateCharField(help_text='Date in YYYY-MM-DD format, use 00 to denote month/day ranges', max_length=10, validators=[daat.maps.utils.partial_date_validator])),
                ('end_date', daat.maps.models.PartialDateCharField(help_text='Date in YYYY-MM-DD format, use 00 to denote month/day ranges', max_length=10, validators=[daat.maps.utils.partial_date_validator], blank=True)),
                ('map_context', models.CharField(max_length=20, choices=[('neighbourhood', 'Neighbourhood'), ('city', 'City'), ('province', 'Province'), ('country', 'Country'), ('continent', 'Continent'), ('world', 'World')], blank=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('deleted', models.BooleanField(default=False)),
                ('file', s3direct.fields.S3DirectField()),
                ('title', models.CharField(max_length=120)),
                ('category', models.CharField(max_length=50, choices=[('manuscript', 'Manuscript'), ('music_score', 'Music Score'), ('song', 'Song'), ('story', 'Story'), ('photograph', 'Photograph')])),
                ('source', models.CharField(max_length=200, blank=True)),
                ('source_url', models.CharField(max_length=500, blank=True)),
                ('copyrights', models.CharField(help_text='For no copyrights use "Public Domain"', max_length=200)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'verbose_name_plural': 'media',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=150)),
                ('alt_name', models.CharField(max_length=150, blank=True)),
                ('description', models.TextField(blank=True)),
                ('type', models.CharField(max_length=200, blank=True)),
                ('start_date', daat.maps.models.PartialDateCharField(help_text='Date in YYYY-MM-DD format, use 00 to denote month/day ranges', max_length=10, validators=[daat.maps.utils.partial_date_validator])),
                ('end_date', daat.maps.models.PartialDateCharField(help_text='Date in YYYY-MM-DD format, use 00 to denote month/day ranges', max_length=10, validators=[daat.maps.utils.partial_date_validator], blank=True)),
                ('cover_image', models.ForeignKey(blank=True, null=True, to='maps.Media')),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('deleted', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=50, blank=True)),
                ('first_name', models.CharField(max_length=120)),
                ('middle_name', models.CharField(max_length=50, blank=True)),
                ('last_name', models.CharField(max_length=150)),
                ('hebrew_name', models.CharField(max_length=200, blank=True)),
                ('nickname', models.CharField(max_length=150, blank=True)),
                ('birth_date', daat.maps.models.PartialDateCharField(help_text='Date in YYYY-MM-DD format, use 00 to denote month/day ranges', max_length=10, validators=[daat.maps.utils.partial_date_validator])),
                ('death_date', daat.maps.models.PartialDateCharField(help_text='Date in YYYY-MM-DD format, use 00 to denote month/day ranges', max_length=10, validators=[daat.maps.utils.partial_date_validator], blank=True)),
                ('biography', models.TextField(blank=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=200)),
                ('alt_name', django.contrib.postgres.fields.ArrayField(help_text='Single alt name with no commas, or comma-separated list of names (e.g. <code>Tel-Aviv,Tel Aviv,תל אביב)</code>', base_field=models.CharField(max_length=300), size=None, blank=True, null=True)),
                ('position', geoposition.fields.GeopositionField(max_length=42)),
                ('area', django.contrib.postgres.fields.hstore.HStoreField(help_text='Paste any custom <a href="http://geojson.io">GeoJSON</a> here', blank=True, null=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('deleted', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=150)),
                ('subtitle', models.CharField(max_length=150, blank=True)),
                ('institution', models.CharField(max_length=200, blank=True)),
                ('supported_by', models.CharField(max_length=200, blank=True)),
                ('research_field', models.CharField(max_length=200, blank=True)),
                ('synopsis', models.TextField(blank=True)),
                ('start_date', daat.maps.models.PartialDateCharField(help_text='Date in YYYY-MM-DD format, use 00 to denote month/day ranges', max_length=10, validators=[daat.maps.utils.partial_date_validator])),
                ('end_date', daat.maps.models.PartialDateCharField(help_text='Date in YYYY-MM-DD format, use 00 to denote month/day ranges', max_length=10, validators=[daat.maps.utils.partial_date_validator], blank=True)),
                ('cover_image', models.ForeignKey(blank=True, null=True, to='maps.Media')),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('deleted', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=50, blank=True)),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=150)),
                ('affiliation', models.CharField(max_length=150, blank=True)),
                ('biography', models.TextField(blank=True)),
                ('profile_image', models.FileField(upload_to='researcher_profiles', null=True, blank=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='project',
            name='researchers',
            field=models.ManyToManyField(to='maps.Researcher', blank=True, related_name='projects'),
        ),
        migrations.AddField(
            model_name='person',
            name='places',
            field=models.ManyToManyField(to='maps.Place', blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='profile_image',
            field=models.ForeignKey(blank=True, null=True, to='maps.Media'),
        ),
        migrations.AddField(
            model_name='organization',
            name='places',
            field=models.ManyToManyField(to='maps.Place', blank=True, related_name='organizations'),
        ),
        migrations.AddField(
            model_name='event',
            name='media',
            field=models.ManyToManyField(to='maps.Media', blank=True, related_name='events'),
        ),
        migrations.AddField(
            model_name='event',
            name='next_event',
            field=models.ForeignKey(blank=True, null=True, to='maps.Event'),
        ),
        migrations.AddField(
            model_name='event',
            name='organizations',
            field=models.ManyToManyField(to='maps.Organization', blank=True, related_name='events'),
        ),
        migrations.AddField(
            model_name='event',
            name='people',
            field=models.ManyToManyField(to='maps.Person', blank=True, related_name='events'),
        ),
        migrations.AddField(
            model_name='event',
            name='place',
            field=models.ForeignKey(to='maps.Place', related_name='events'),
        ),
        migrations.AddField(
            model_name='event',
            name='project',
            field=models.ForeignKey(to='maps.Project', related_name='events'),
        ),
        migrations.AddField(
            model_name='annotation',
            name='events',
            field=models.ManyToManyField(to='maps.Event', related_name='annotations'),
        ),
        migrations.AddField(
            model_name='annotation',
            name='origin',
            field=models.ForeignKey(blank=True, null=True, to='maps.Place'),
        ),
        migrations.AddField(
            model_name='annotation',
            name='places',
            field=models.ManyToManyField(to='maps.Place', blank=True, related_name='annotations'),
        ),
    ]
