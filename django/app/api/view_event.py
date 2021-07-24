# coding=utf-8
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import permission_classes, action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
import datetime
from .models import Event, Brand, SubscribeEvent
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
            - GET /api/events
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

    @action(detail=False, methods=['post'])
    def get_onoff(self, request):
        data = JSONParser().parse(request)
        brand_id = data['brand_id']
        now = datetime.datetime.now()
        # 하트순 정렬 하려면 _order_by로 못하고 하트인거랑 아닌거 나눠서 해야할듯
        off = Event.objects.filter(brand=brand_id, due__lte=now)
        on = Event.objects.filter(brand=brand_id, due__gt=now)
        off_event = off.values()
        on_event = on.values()
        return JsonResponse({'on_event': list(on_event),
                             'off_event': list(off_event)}, status=200)

    @action(detail=False, methods=['post'])
    def get_main(self, request):
        data = JSONParser().parse(request)
        category_id = data['category_id']
        user_id = data['user_id']
        events = Event.objects.filter(category=category_id)
        subscribes = SubscribeEvent.objects.filter(user=user_id)
        subscribe = []
        for i in events:
            for j in subscribes:
                if i.id == j.event.id:
                    subscribe.append("Yes")
                    break
            else:
                subscribe.append("No")
        event = events.values()
        return JsonResponse({'event': list(event),
                             'subscribe': subscribe}, status=200)
