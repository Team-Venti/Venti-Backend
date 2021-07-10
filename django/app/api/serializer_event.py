from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
