from rest_framework import serializers

from .models import *


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id', 'name', 'position')


class EventSerializer(serializers.ModelSerializer):
    place = PlaceSerializer(read_only=True)
    icon = serializers.FileField(use_url=True)
    class Meta:
        model = Event
        fields = ('id', 'title', 'subtitle', 'start_date', 'end_date', 'place', 'description', 'icon')
