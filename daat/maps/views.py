from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework_extensions.cache.decorators import cache_response

from .models import *
from .serializers import *


class CacheViewSet(viewsets.ReadOnlyModelViewSet):
    @cache_response()
    def list(self, request):
        response = super(CacheViewSet, self).list(request)
        response['Cache-Control'] = 'public, max-age=36000000'

        return response


class EventViewSet(CacheViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = self.queryset
        proj_id = self.request.query_params.get('project', None)
        if proj_id is not None:
            queryset = queryset.filter(project_id=proj_id)

        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class ProjectViewSet(CacheViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class AnnotationViewSet(CacheViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer


class PlaceViewSet(CacheViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class PersonViewSet(CacheViewSet):
    queryset = Person.objects.all()
    serializer_class = FullPersonSerializer


class OrganizationViewSet(CacheViewSet):
    queryset = Organization.objects.all()
    serializer_class = FullOrganizationSerializer




