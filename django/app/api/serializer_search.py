from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .serializer_brand import BrandSerializer
from .models import Event


class SearchSerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'image', 'due', 'weekly_view', 'brands']
