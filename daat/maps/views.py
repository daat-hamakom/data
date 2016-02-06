from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets

from .models import *
from .serializers import *


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class SpriteJsonView(View):
    def get(self, *args, **kwargs):
        return JsonResponse(cache.get('sprites:json'))

class SpritePngView(View):
    def get(self, *args, **kwargs):
        response = HttpResponse(cache.get('sprites:png').seek(0).read())
        response['Content-Type'] = 'image/png'
        return response
