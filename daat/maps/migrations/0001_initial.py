# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import daat.maps.models
import daat.maps.utils


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=20, choices=[('correspondence', 'Correspondence'), ('group', 'Group'), ('travel', 'Travel'), ('trend', 'Trend')])),
                ('description', models.TextField(blank=True)),
                ('link_style', models.CharField(max_length=20, choices=[('path', 'Path'), ('correspondence', 'Correspondence'), ('flow', 'Flow')])),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=160)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.CharField(validators=[daat.maps.utils.partial_date_validator], max_length=10)),
                ('end_date', models.CharField(blank=True, validators=[daat.maps.utils.partial_date_validator], max_length=10)),
                ('map_context', models.CharField(blank=True, max_length=20, choices=[('neighbourhood', 'Neighbourhood'), ('city', 'City'), ('province', 'Province'), ('country', 'Country'), ('continent', 'Continent'), ('world', 'World')])),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to=daat.maps.models.concat_category)),
                ('title', models.CharField(max_length=120)),
                ('category', models.CharField(max_length=50, choices=[('manuscript', 'Manuscript'), ('music_score', 'Music Score'), ('song', 'Song'), ('story', 'Story'), ('photograph', 'Photograph')])),
                ('source', models.CharField(blank=True, max_length=200)),
                ('source_url', models.CharField(blank=True, max_length=500)),
                ('copyrights', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('alt_name', models.CharField(blank=True, max_length=150)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.CharField(validators=[daat.maps.utils.partial_date_validator], max_length=10)),
                ('end_date', models.CharField(blank=True, validators=[daat.maps.utils.partial_date_validator], max_length=10)),
                ('cover_image', models.ForeignKey(to='maps.Media', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=50)),
                ('first_name', models.CharField(max_length=120)),
                ('middle_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(max_length=150)),
                ('nickname', models.CharField(blank=True, max_length=150)),
                ('birth_date', models.CharField(validators=[daat.maps.utils.partial_date_validator], max_length=10)),
                ('death_date', models.CharField(blank=True, validators=[daat.maps.utils.partial_date_validator], max_length=10)),
                ('biography', models.TextField(blank=True)),
                ('profile_image', models.ForeignKey(to='maps.Media', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('synopsis', models.TextField(blank=True)),
                ('start_date', models.CharField(validators=[daat.maps.utils.partial_date_validator], max_length=10)),
                ('end_date', models.CharField(blank=True, validators=[daat.maps.utils.partial_date_validator], max_length=10)),
                ('cover_image', models.ForeignKey(to='maps.Media', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=50)),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=150)),
                ('biography', models.TextField(blank=True)),
                ('profile_image', models.FileField(null=True, blank=True, upload_to='researcher_profiles')),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='places',
            field=models.ManyToManyField(to='maps.Place', related_name='organizations'),
        ),
        migrations.AddField(
            model_name='event',
            name='media',
            field=models.ManyToManyField(to='maps.Media', related_name='events'),
        ),
        migrations.AddField(
            model_name='event',
            name='organizations',
            field=models.ManyToManyField(to='maps.Organization', related_name='events'),
        ),
        migrations.AddField(
            model_name='event',
            name='people',
            field=models.ManyToManyField(to='maps.Person', related_name='events'),
        ),
        migrations.AddField(
            model_name='event',
            name='place',
            field=models.ForeignKey(to='maps.Place', related_name='events'),
        ),
        migrations.AddField(
            model_name='annotation',
            name='events',
            field=models.ManyToManyField(to='maps.Event', related_name='annotations'),
        ),
        migrations.AddField(
            model_name='annotation',
            name='places',
            field=models.ManyToManyField(to='maps.Place', related_name='annotations'),
        ),
    ]
