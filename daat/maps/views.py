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

    def get_queryset(self):
        queryset = self.queryset
        proj_id = self.request.query_params.get('project', None)
        if proj_id is not None:
            queryset = queryset.filter(project_id=proj_id)
        return queryset


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class AnnotationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
