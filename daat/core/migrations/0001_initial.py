# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import django.utils.timezone
import django.core.validators
import daat.core.utils


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='DaatUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], error_messages={'unique': 'A user with that username already exists.'})),
                ('first_name', models.CharField(verbose_name='first name', max_length=30, blank=True)),
                ('last_name', models.CharField(verbose_name='last name', max_length=30, blank=True)),
                ('email', models.EmailField(verbose_name='email address', max_length=254, blank=True)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', verbose_name='staff status', default=False)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', to='auth.Group', verbose_name='groups', related_name='user_set', related_query_name='user', blank=True)),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', to='auth.Permission', verbose_name='user permissions', related_name='user_set', related_query_name='user', blank=True)),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=160)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.CharField(validators=[daat.core.utils.partial_date_validator], max_length=10)),
                ('end_date', models.CharField(validators=[daat.core.utils.partial_date_validator], max_length=10, blank=True)),
                ('map_context', models.CharField(blank=True, max_length=20, choices=[('neighbourhood', 'Neighbourhood'), ('city', 'City'), ('province', 'Province'), ('country', 'Country'), ('continent', 'Continent'), ('world', 'World')])),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('file', models.FileField(upload_to='')),
                ('title', models.CharField(max_length=120)),
                ('category', models.CharField(max_length=50, choices=[('manuscript', 'Manuscript'), ('music_score', 'Music Score'), ('song', 'Song'), ('story', 'Story'), ('photograph', 'Photograph')])),
                ('source', models.CharField(max_length=200, blank=True)),
                ('source_url', models.CharField(max_length=500, blank=True)),
                ('copyrights', models.CharField(max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('alt_name', models.CharField(max_length=150, blank=True)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.CharField(validators=[daat.core.utils.partial_date_validator], max_length=10)),
                ('end_date', models.CharField(validators=[daat.core.utils.partial_date_validator], max_length=10, blank=True)),
                ('cover_image', models.ForeignKey(to='core.Media', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=50, blank=True)),
                ('first_name', models.CharField(max_length=120)),
                ('middle_name', models.CharField(max_length=50, blank=True)),
                ('last_name', models.CharField(max_length=150)),
                ('nickname', models.CharField(max_length=150, blank=True)),
                ('birth_date', models.CharField(validators=[daat.core.utils.partial_date_validator], max_length=10)),
                ('death_date', models.CharField(validators=[daat.core.utils.partial_date_validator], max_length=10, blank=True)),
                ('biography', models.TextField(blank=True)),
                ('profile_image', models.ForeignKey(to='core.Media', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('synopsis', models.TextField(blank=True)),
                ('start_date', models.CharField(validators=[daat.core.utils.partial_date_validator], max_length=10)),
                ('end_date', models.CharField(validators=[daat.core.utils.partial_date_validator], max_length=10, blank=True)),
                ('cover_image', models.ForeignKey(to='core.Media', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='places',
            field=models.ManyToManyField(related_name='organizations', to='core.Place'),
        ),
        migrations.AddField(
            model_name='event',
            name='media',
            field=models.ManyToManyField(related_name='events', to='core.Media'),
        ),
        migrations.AddField(
            model_name='event',
            name='organizations',
            field=models.ManyToManyField(related_name='events', to='core.Organization'),
        ),
        migrations.AddField(
            model_name='event',
            name='people',
            field=models.ManyToManyField(related_name='events', to='core.Person'),
        ),
        migrations.AddField(
            model_name='event',
            name='place',
            field=models.ForeignKey(to='core.Place', related_name='events'),
        ),
    ]
