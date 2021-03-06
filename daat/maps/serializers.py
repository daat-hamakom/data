from rest_framework import serializers

from .models import *


class PlaceSerializer(serializers.ModelSerializer):
    events_count = serializers.SerializerMethodField()

    def get_events_count(self, obj):
        queryset = obj.events
        dataset = self.context['request'].query_params.get('dataset', None)
        if dataset is not None:
            dataset_obj = DataSet.objects.filter(url=dataset).first()
            if dataset_obj and dataset_obj.name != 'Draft':
                queryset = queryset.filter(data_sets__in=[dataset_obj.id])
        return queryset.count()

    class Meta:
        model = Place
        fields = ('id', 'name', 'position', 'zoomlevel', 'alt_name', 'events_count')


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('id', 'first_name', 'middle_name', 'last_name')


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('file', 'type', 'url', 'title', 'source', 'source_url', 'copyrights')


class ProjectSerializer(serializers.ModelSerializer):
    researchers = serializers.SlugRelatedField(read_only=True, many=True, slug_field='name')
    cover_image = MediaSerializer(read_only=True)
    events_count = serializers.SerializerMethodField()

    def get_events_count(self, obj):
        queryset = obj.events
        dataset = self.context['request'].query_params.get('dataset', None)
        if dataset is not None:
            dataset_obj = DataSet.objects.filter(url=dataset).first()
            if dataset_obj and dataset_obj.name != 'Draft':
                queryset = queryset.filter(data_sets__in=[dataset_obj.id])
        return queryset.count()

    class Meta:
        model = Project


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name')


class EventSerializer(serializers.ModelSerializer):

    place = PlaceSerializer(read_only=True)
    people = PersonSerializer(read_only=True, many=True)
    organizations = OrganizationSerializer(read_only=True, many=True)
    media = MediaSerializer(read_only=True, many=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'subtitle', 'start_date', 'end_date', 'circa_date', 'place',
            'description', 'icon', 'map_context', 'project', 'people', 'organizations', 'media', 'tags')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('place')
        queryset = queryset.prefetch_related('people', 'organizations', 'media')
        return queryset


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        exclude = ('deleted', 'published')


class FullPersonSerializer(serializers.ModelSerializer):
    profile_image = MediaSerializer(read_only=True)
    places = serializers.SlugRelatedField(read_only=True, many=True, slug_field='name')
    events_count = serializers.SerializerMethodField()

    def get_events_count(self, obj):
        queryset = obj.events
        dataset = self.context['request'].query_params.get('dataset', None)
        if dataset is not None:
            dataset_obj = DataSet.objects.filter(url=dataset).first()
            if dataset_obj and dataset_obj.name != 'Draft':
                queryset = queryset.filter(data_sets__in=[dataset_obj.id])
        return queryset.count()

    class Meta:
        model = Person
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'title', 'alt_name',
                  'birth_date', 'death_date', 'biography', 'profile_image', 'places', 'events_count')


class FullOrganizationSerializer(serializers.ModelSerializer):
    cover_image = MediaSerializer(read_only=True)
    places = serializers.SlugRelatedField(read_only=True, many=True, slug_field='name')
    events_count = serializers.SerializerMethodField()

    def get_events_count(self, obj):
        queryset = obj.events
        dataset = self.context['request'].query_params.get('dataset', None)
        if dataset is not None:
            dataset_obj = DataSet.objects.filter(url=dataset).first()
            if dataset_obj and dataset_obj.name != 'Draft':
                queryset = queryset.filter(data_sets__in=[dataset_obj.id])
        return queryset.count()

    class Meta:
        model = Organization
        fields = ('id', 'name', 'alt_name', 'type', 'start_date', 'end_date', 'description',
                  'cover_image', 'places', 'events_count')
