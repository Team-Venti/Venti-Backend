from rest_framework import viewsets
from .models import Event
from .serializer_search import SearchSerializer
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend

# 검색 - 미완


class SearchFilter(FilterSet):
    description = filters.CharFilter(field_name="description", lookup_expr="icontains")
    brand = filters.CharFilter(field_name="brand")
    event = filters.NumberFilter(field_name="id")

    class Meta:
        model = Event
        fields = ['category', 'brand', 'event']


class SearchViewSet(viewsets.ModelViewSet):
    serializer_class = SearchSerializer
    queryset = Event.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SearchFilter
