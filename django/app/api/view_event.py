from rest_framework import viewsets
from .models import Event
from .serializer_event import EventSerializer
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend

# 이벤트 메인, 이벤트 필터, 브랜드 상세, 이벤트 상세


class EventFilter(FilterSet):
    category = filters.NumberFilter(field_name="category")
    brand = filters.NumberFilter(field_name="brand")
    event = filters.NumberFilter(field_name="id")

    class Meta:
        model = Event
        fields = ['category', 'brand', 'event']


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EventFilter
