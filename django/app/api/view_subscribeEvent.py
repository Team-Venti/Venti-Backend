from rest_framework import viewsets
from .models import SubscribeEvent
from .serializer_subscribeEvent import SubscribeEventSerializer
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend

# 이벤트 좋아요 버튼, 마이브랜드_이벤트


class SubscribeEventFilter(FilterSet):
    user = filters.NumberFilter(field_name="user")

    class Meta:
        model = SubscribeEvent
        fields = ['user']


class SubscribeEventViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeEventSerializer
    queryset = SubscribeEvent.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SubscribeEventFilter
