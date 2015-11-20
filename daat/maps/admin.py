from ckeditor.fields import RichTextField
from django.contrib import admin
from django.forms import ModelForm, TextInput
from django.db import models

from .models import *


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = 'Mark selected events as published'


class CreatorMixin(object):
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()


class EventAdmin(CreatorMixin, admin.ModelAdmin):
    list_display = ('title', 'description', 'start_date', 'end_date', 'project', 'published')
    list_filter = ('project', 'published')
    exclude = ('deleted',)
    actions = [make_published]
    save_as = True


class MediaAdmin(CreatorMixin, admin.ModelAdmin):
    exclude = ('deleted',)


class OrganizationAdmin(CreatorMixin, admin.ModelAdmin):
    exclude = ('deleted',)


class PersonAdmin(CreatorMixin, admin.ModelAdmin):
    exclude = ('deleted',)


class PlaceAdmin(CreatorMixin, admin.ModelAdmin):
    exclude = ('deleted',)


class ProjectAdmin(CreatorMixin, admin.ModelAdmin):
    exclude = ('deleted',)


class ResearcherAdmin(CreatorMixin, admin.ModelAdmin):
    exclude = ('deleted',)


class AnnotationAdmin(CreatorMixin, admin.ModelAdmin):
    list_filter = ('events', 'events__project', 'published')
    exclude = ('deleted',)
    actions = [make_published]
    save_as = True


admin.site.register(Event, EventAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Researcher, ResearcherAdmin)
admin.site.register(Annotation, AnnotationAdmin)
