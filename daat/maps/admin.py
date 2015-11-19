from ckeditor.fields import RichTextField
from django.contrib import admin
from django.forms import ModelForm, TextInput
from django.db import models

from .models import *


class LargeTextInputMixin(object):
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'size': '80'})
        },
    }


class LargeTextInputAdmin(LargeTextInputMixin, admin.ModelAdmin):
    pass


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = 'Mark selected events as published'


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'start_date', 'end_date', 'project', 'published')
    list_filter = ('project', 'published')
    actions = [make_published]
    save_as = True


admin.site.register(Event, EventAdmin)
admin.site.register(Media)
admin.site.register(Organization)
admin.site.register(Person)
admin.site.register(Place)
admin.site.register(Project)
admin.site.register(Researcher)
admin.site.register(Annotation)
