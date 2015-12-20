from ckeditor.fields import RichTextField
from django.contrib import admin
from django.forms import ModelForm, TextInput
from django.db import models

from .models import *


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = 'Mark selected events as published'


class CreatorMixin(object):

    readonly_fields = ('creator',)

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
        obj.save()


class EventAdmin(CreatorMixin, admin.ModelAdmin):
    list_display = ('title', 'project', 'place', 'start_date', 'end_date', 'published')
    list_filter = ('creator', 'project', 'published')
    filter_horizontal = ('people', 'organizations', 'media',)
    exclude = ('deleted',)
    actions = [make_published]
    save_as = True


class MediaAdmin(CreatorMixin, admin.ModelAdmin):
    list_display = ('title', 'filename', 'url', 'type', 'source', 'copyrights')
    list_filter = ('type', 'events__project', 'creator')
    exclude = ('deleted', 'type',)


class OrganizationAdmin(CreatorMixin, admin.ModelAdmin):
    list_display = ('name', 'type')
    list_filter = ('creator',)
    filter_horizontal = ('places',)
    exclude = ('deleted',)


class PersonAdmin(CreatorMixin, admin.ModelAdmin):
    list_display = ('last_name', 'title', 'first_name')
    list_filter = ('creator',)
    filter_horizontal = ('places',)
    exclude = ('deleted',)


class PlaceAdmin(CreatorMixin, admin.ModelAdmin):
    exclude = ('deleted',)


class ProjectAdmin(CreatorMixin, admin.ModelAdmin):
    list_display = ('title', 'subtitle')
    list_filter = ('creator', 'researchers')
    filter_horizontal = ('researchers',)
    exclude = ('deleted',)


class ResearcherAdmin(CreatorMixin, admin.ModelAdmin):
    exclude = ('deleted',)


class AnnotationAdmin(CreatorMixin, admin.ModelAdmin):
    list_display = ('all_events', 'type', 'published')
    list_filter = ('events', 'events__project', 'published', 'creator')
    filter_horizontal = ('places', 'events',)
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
