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
    """
        유저의 이벤트 좋아요 목록을 불러오거나 저장/삭제 하는 API
        ---
        # 예시
            - GET /api/myevents/
            - GET /api/myevents/?user=2
            - POST /api/myevents/
            - DELETE /api/myevents/{id}
        # parameter
            - user : 어떤 유저가 좋아요 했는지 (Foreign Key)
            - event : 어떤 이벤트를 좋아요 했는지 (Foreign Key)
    """
    serializer_class = SubscribeEventSerializer
    queryset = SubscribeEvent.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SubscribeEventFilter
