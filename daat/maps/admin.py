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
        obj.creator = request.user
        obj.save()


class EventAdmin(CreatorMixin, admin.ModelAdmin):
    list_display = ('title', 'project', 'place', 'start_date', 'end_date', 'published')
    list_filter = ('creator', 'project', 'published')
    exclude = ('deleted',)
    actions = [make_published]
    save_as = True


class MediaAdmin(CreatorMixin, admin.ModelAdmin):
    list_display = ('file', 'title', 'type', 'source', 'copyrights')
    list_filter = ('type', 'creator')
    exclude = ('deleted',)


class OrganizationAdmin(CreatorMixin, admin.ModelAdmin):
    exclude = ('deleted',)


class PersonAdmin(CreatorMixin, admin.ModelAdmin):
    list_display = ('title', 'first_name', 'last_name', 'hebrew_name')
    list_filter = ('creator',)
    exclude = ('deleted',)


class PlaceAdmin(CreatorMixin, admin.ModelAdmin):
    exclude = ('deleted',)


class ProjectAdmin(CreatorMixin, admin.ModelAdmin):
    list_display = ('title', 'subtitle')
    list_filter = ('creator', 'researchers')
    exclude = ('deleted',)


class ResearcherAdmin(CreatorMixin, admin.ModelAdmin):
    exclude = ('deleted',)


class AnnotationAdmin(CreatorMixin, admin.ModelAdmin):
    list_display = ('type', 'published')
    list_filter = ('events', 'events__project', 'published', 'creator')
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
