from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import SubscribeBrand


class SubscribeBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribeBrand
        fields = '__all__'
