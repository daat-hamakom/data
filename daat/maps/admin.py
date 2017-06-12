from ckeditor.fields import RichTextField
import re
import html
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.forms import ModelForm, TextInput, ChoiceField
from django.db import models
from django_select2.forms import Select2Widget, Select2TagWidget

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
        if not selected_choices:
            return ''
        options = [x.replace('|', ',') for x in selected_choices.split(',')]
        return '\n'.join([OPTION_SELECTED.format(opt, opt) for opt in options])


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ('deleted', 'subtitle', )
        widgets = {
            'place': Select2Widget,
            'next_event': Select2Widget,
            'tags': ArrayTagWidget
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['media_icon'].queryset = Media.objects.filter(events__id=self.instance.pk)


class EventAdmin(CreatorMixin, admin.ModelAdmin):

    class Media:
        js = ('//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.4/jquery.min.js',)
        css = {'all': ('/static/stylesheets/admin.css', ) }

    def words_count(self):
        try:
            cleanr = re.compile('<.*?>')
            cleantext = re.sub(cleanr, '', html.unescape(self.description))

            return len(' '.join([self.title, cleantext]).split())
        except Exception:
            return '?'
    words_count.short_description = 'Word Count'

    list_display = ('title', 'project', 'place', 'start_date', 'end_date', 'published', 'edit_mode', words_count)
    list_filter = ('project', 'published', 'creator')
    filter_horizontal = ('people', 'organizations', 'media',)
    exclude = ('deleted', 'subtitle')
    actions = [make_published]
    save_as = True
    form = EventForm


class MediaAdmin(CreatorMixin, admin.ModelAdmin):

    class Media:
        css = {'all': ('/static/stylesheets/admin.css',)}

    list_display = ('title', 'filename', 'url', 'type', 'source', 'copyrights')
    list_filter = ('type', 'events__project', 'creator')
    exclude = ('deleted', 'type',)


class OrganizationAdmin(CreatorMixin, admin.ModelAdmin):

    class Media:
        css = {'all': ('/static/stylesheets/admin.css',)}

    def words_count(self):
        try:
            cleanr = re.compile('<.*?>')
            cleantext = re.sub(cleanr, '', html.unescape(self.description))

            return len(cleantext.split())
        except Exception:
            return '?'
    words_count.short_description = 'Word Count'

    list_display = ('name', 'type', 'viaf_id', 'edit_mode', words_count)
    list_filter = ('creator',)
    filter_horizontal = ('places',)
    exclude = ('deleted',)


class PersonAdmin(CreatorMixin, admin.ModelAdmin):

    class Media:
        js = ('//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.4/jquery.min.js',)
        css = {'all': ('/static/stylesheets/admin.css',)}

    def words_count(self):
        try:
            cleanr = re.compile('<.*?>')
            cleantext = re.sub(cleanr, '', html.unescape(self.biography))

            return len(cleantext.split())
        except Exception:
            return '?'
    words_count.short_description = 'Word Count'

    list_display = ('id', 'last_name', 'first_name', 'viaf_id', 'edit_mode', words_count)
    list_filter = ('creator',)
    filter_horizontal = ('places',)
    exclude = ('deleted',)
    formfield_overrides = {
        ArrayField: {
            'widget': ArrayTagWidget
        },
        models.ForeignKey: {
            'widget': Select2Widget
        }
    }


class PlaceAdmin(CreatorMixin, admin.ModelAdmin):

    class Media:
        js = ('//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.4/jquery.min.js',)
        css = {'all': ('/static/stylesheets/admin.css',)}

    list_display = ('id', 'name', 'zoomlevel', 'viaf_id')
    exclude = ('deleted',)
    formfield_overrides = {
        ArrayField: {
            'widget': ArrayTagWidget
        },
    }


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ('deleted',)
        widgets = {
            'cover_image': Select2Widget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cover_image'].required = True
        self.fields['researchers'].required = True
        self.fields['synopsis'].required = True


class ProjectAdmin(CreatorMixin, admin.ModelAdmin):

    class Media:
        js = ('//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.4/jquery.min.js',)
        css = {'all': ('/static/stylesheets/admin.css',)}

    def words_count(self):
        try:
            cleanr = re.compile('<.*?>')
            cleantext = re.sub(cleanr, '', html.unescape(self.synopsis))

            return len(' '.join([self.title, self.subtitle, cleantext]).split())
        except Exception:
            return '?'
    words_count.short_description = 'Word Count'

    list_display = ('title', 'subtitle', 'edit_mode', words_count)
    list_filter = ('researchers', 'creator')
    filter_horizontal = ('researchers',)
    form = ProjectForm


class ResearcherAdmin(CreatorMixin, admin.ModelAdmin):
    exclude = ('deleted',)


class AnnotationAdmin(CreatorMixin, admin.ModelAdmin):

    class Media:
        js = ('//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.4/jquery.min.js',)
        css = {'all': ('/static/stylesheets/admin.css',)}

    list_display = ('all_events', 'type', 'published')
    list_filter = ('events__project', 'published', 'creator')
    filter_horizontal = ('places', 'events', 'media')
    exclude = ('deleted', 'media')
    actions = [make_published]
    save_as = True

    formfield_overrides = {
        models.ForeignKey: {
            'widget': Select2Widget
        },
    }


class ImportAdmin(CreatorMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'target_project', 'status')
    exclude = ('deleted',)
    readonly_fields = ('status', 'error_log')


admin.site.register(Event, EventAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Researcher, ResearcherAdmin)
admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Import, ImportAdmin)
