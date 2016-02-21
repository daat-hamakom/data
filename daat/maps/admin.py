from ckeditor.fields import RichTextField
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.forms import ModelForm, TextInput
from django.db import models
from django_select2.forms import Select2TagWidget

from .models import *


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = 'Mark selected events as published'


class CreatorMixin(object):

    readonly_fields = ('creator',)

    def save_model(self, request, obj, form, change):
        if not obj.creator_id:  # when we test for creator RelatedObjectDoesNotExist is thrown :/
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


class ArrayTagWidget(Select2TagWidget):

    def build_attrs(self, extra_attrs=None, **kwargs):
        self.attrs.setdefault('data-token-separators', [])
        self.attrs.setdefault('data-width', '500px')
        self.attrs.setdefault('data-tags', 'true')
        return super().build_attrs(extra_attrs, **kwargs)

    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)
        return ','.join([x.replace(',', '|') for x in values])

    def render_options(self, choices, selected_choices):
        OPTION_SELECTED = '<option selected="selected" value="{}">{}</option>'
        options = [x.replace('|', ',') for x in selected_choices.split(',')]
        return '\n'.join([OPTION_SELECTED.format(opt, opt) for opt in options])


class PlaceAdmin(CreatorMixin, admin.ModelAdmin):

    class Media:
        js = ('//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.4/jquery.min.js',)

    exclude = ('deleted',)
    formfield_overrides = {
        ArrayField: {
            'widget': ArrayTagWidget
        },
    }


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
    filter_horizontal = ('places', 'events', 'media')
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
