from rest_framework import viewsets
from .models import Event, SubscribeEvent
from .serializer_event import EventSerializer, EventForYouSerializer
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
    """
        이벤트 목록을 불러오거나 저장/수정/삭제 하는 API
        ---
        # 내용
            - name : 이벤트 이름
            - image : 이벤트 대표 이미지
            - banner_image : '인기 이벤트'에 띄우기 위한 크기가 다른 이미지
            - text : 이벤트 설명
            - due : 이벤트 마감 기한
            - weekly_view : 주간 조회수
            - url : 기업의 이벤트 페이지로 이동하기 위한 url
            - category : 이벤트가 속한 카테고리(Foreign Key)
            - brand : 이벤트가 속한 브랜드(Foreign Key)
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EventFilter
