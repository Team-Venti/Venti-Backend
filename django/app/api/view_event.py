# coding=utf-8
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from .models import Event, Brand
from .serializer_event import EventSerializer, EventForYouSerializer
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend
# jwt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


# 이벤트 메인, 이벤트 필터, 브랜드 상세, 이벤트 상세


class EventFilter(FilterSet):
    category = filters.NumberFilter(field_name="category")
    brand = filters.CharFilter(method='brand_filter')

    class Meta:
        model = Event
        fields = ['category', 'brand']

    def brand_filter(self, queryset, name, value):
        qs0 = queryset.filter(brand=0)  # 빈 쿼리셋
        for i in range(len(value)):
            if i % 2 == 1:
                qs1 = queryset.filter(brand=value[i])
                qs0 = qs0.union(qs1)
        filtered_queryset = qs0
        return filtered_queryset


@permission_classes([IsAuthenticated,])
@authentication_classes([JSONWebTokenAuthentication,])
class EventViewSet(viewsets.ModelViewSet):
    """
        이벤트 목록을 불러오거나 저장/수정/삭제 하는 API
        ---
        # 예시
            - GET /api/events/
            - GET /api/events/?catogory=1
            - GET /api/events/?brand=[1,3,5]
            - GET /api/events/{id}
        # parameter
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
