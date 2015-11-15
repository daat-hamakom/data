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

admin.site.register(Event)
admin.site.register(Media)
admin.site.register(Organization)
admin.site.register(Person)
admin.site.register(Place)
admin.site.register(Project)
admin.site.register(Researcher)
admin.site.register(Annotation)
