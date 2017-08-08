from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.db.models import Count

from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.utils import default_cache_key_func
from .models import *
from .serializers import *
import time

MAX_CACHE_TIME = 3600


#  todo - investigate why the timeout dont work
class CacheViewSet(viewsets.ReadOnlyModelViewSet):
    @cache_response(MAX_CACHE_TIME * 1,  key_func='calculate_cache_key')
    def list(self, request):
        response = super(CacheViewSet, self).list(request)
        # response['Cache-Control'] = 'public, max-age=' + str(MAX_CACHE_TIME)

        return response

    # hotfix - timeout doesnt work
    def calculate_cache_key(self, view_instance, view_method,
                                request, args, kwargs):
        print(request.path + '?' + request.GET.urlencode())
        return request.path + '?' + request.GET.urlencode()


class EventViewSet(CacheViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = self.queryset
        proj_id = self.request.query_params.get('project', None)
        if proj_id is not None:
            queryset = queryset.filter(project_id=proj_id)

        dataset = self.request.query_params.get('dataset', None)
        if dataset is not None:
            dataset_obj = DataSet.objects.filter(url=dataset).first()
            if dataset_obj and dataset_obj.name != 'Draft':
                queryset = queryset.filter(data_sets__in=[dataset_obj.id])

        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class ProjectViewSet(CacheViewSet):
    queryset = Project.objects.annotate(num_events=Count('events')).exclude(num_events=0)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = self.queryset

        dataset = self.request.query_params.get('dataset', None)
        if dataset is not None:
            dataset_obj = DataSet.objects.filter(url=dataset).first()
            if dataset_obj and dataset_obj.name != 'Draft':
                queryset = queryset.filter(events__data_sets__in=[dataset_obj.id])

        return queryset


class AnnotationViewSet(CacheViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer

    def get_queryset(self):
        queryset = self.queryset

        dataset = self.request.query_params.get('dataset', None)
        if dataset is not None:
            dataset_obj = DataSet.objects.filter(url=dataset).first()
            if dataset_obj and dataset_obj.name != 'Draft':
                queryset = queryset.filter(events__data_sets__in=[dataset_obj.id])

        return queryset


class PlaceViewSet(CacheViewSet):
    queryset = Place.objects.annotate(num_events=Count('events')).exclude(num_events=0)
    serializer_class = PlaceSerializer

    def get_queryset(self):
        queryset = self.queryset

        dataset = self.request.query_params.get('dataset', None)
        if dataset is not None:
            dataset_obj = DataSet.objects.filter(url=dataset).first()
            if dataset_obj and dataset_obj.name != 'Draft':
                queryset = queryset.filter(events__data_sets__in=[dataset_obj.id])

        return queryset


class PersonViewSet(CacheViewSet):
    queryset = Person.objects.annotate(num_events=Count('events')).exclude(num_events=0).order_by('last_name')
    serializer_class = FullPersonSerializer

    def get_queryset(self):
        queryset = self.queryset

        dataset = self.request.query_params.get('dataset', None)
        if dataset is not None:
            dataset_obj = DataSet.objects.filter(url=dataset).first()
            if dataset_obj and dataset_obj.name != 'Draft':
                queryset = queryset.filter(events__data_sets__in=[dataset_obj.id])

        return queryset


class OrganizationViewSet(CacheViewSet):
    queryset = Organization.objects.annotate(num_events=Count('events')).exclude(num_events=0)
    serializer_class = FullOrganizationSerializer

    def get_queryset(self):
        queryset = self.queryset

        dataset = self.request.query_params.get('dataset', None)
        if dataset is not None:
            dataset_obj = DataSet.objects.filter(url=dataset).first()
            if dataset_obj and dataset_obj.name != 'Draft':
                queryset = queryset.filter(events__data_sets__in=[dataset_obj.id])

        return queryset



