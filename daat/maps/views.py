from django.http import HttpResponse
from django.views.generic import View

from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets

from .models import *
from .serializers import *


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class SpriteView(View):
    def get(self, *args, **kwargs):
        response = HttpResponse('hai')
        return response
