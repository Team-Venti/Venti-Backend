from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Event,User,SubscribeEvent


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventSubsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribeEvent
        fields = '__all__'


class EventForYouSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['brand']