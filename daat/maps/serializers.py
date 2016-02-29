from rest_framework import serializers

from .models import *


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id', 'name', 'position')


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'first_name', 'middle_name', 'last_name')


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name')


class MediaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Media
		fields = ('file',)


class EventSerializer(serializers.ModelSerializer):

    place = PlaceSerializer(read_only=True)
    people = PersonSerializer(read_only=True, many=True)
    organizations = OrganizationSerializer(read_only=True, many=True)
    media = MediaSerializer(read_only=True, many=True)
    project = serializers.SlugRelatedField(read_only=True, slug_field='title')

    class Meta:
        model = Event
        fields = ('id', 'title', 'subtitle', 'start_date', 'end_date', 'place',
        	'description', 'icon', 'project', 'people', 'organizations', 'media')
