from rest_framework import viewsets
from .models import Brand, SubscribeBrand
from .serializer_brand import BrandSerializer
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend


# 브랜드


class BrandFilter(FilterSet):
    category = filters.NumberFilter(field_name="category")

    class Meta:
        model = Brand
        fields = ['category']


class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BrandFilter

