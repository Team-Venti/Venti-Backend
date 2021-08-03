# coding=utf-8
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes, action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

from .models import Event, Brand, SubscribeEvent, Notification, SubscribeBrand, User
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


@permission_classes([IsAuthenticated, ])
@authentication_classes([JSONWebTokenAuthentication, ])
class EventViewSet(viewsets.ModelViewSet):
    '''
    회원일때 api
    POST api/events/main/ - 이벤트 메인
    POST api/events/details/ - 이벤트 상세
    POST api/events/deadline/ - 브랜드 상세 눌렀을 때 밑에 이벤트들
    비회원일때 api
    POST api/guest/event_main/ - 이벤트 메인
    POST api/guest/event_detail/ - 이벤트 상세
    POST api/guest/event_deadline/ - 브랜드 상세 눌렀을 때 밑에 이벤트들
    '''
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EventFilter
    # http_method_names = ['get', 'post']

    response_schema_dict3 = {
        "200": openapi.Response(
            description="특정 브랜드의 모든 이벤트 목록과 구독 정보, 진행/마감 정보를 제공하는 API",
            examples={
                "application/json": {
                    "on_event": [
                        {
                            "id": 3,
                            "created_date": "2021-07-11",
                            "update_date": "2021-07-21",
                            "category_id": 1,
                            "brand_id": 1,
                            "name": "vips_Event3",
                            "image": "",
                            "banner_image": "",
                            "text": "vvv",
                            "due": "2021-12-12T00:00:00",
                            "weekly_view": 'null',
                            "url": 'null'
                        }
                    ],
                    "on_subscribe": [
                        "No"
                    ],
                    "off_event": [
                        {
                            "id": 1,
                            "created_date": "2021-07-11",
                            "update_date": "2021-07-21",
                            "category_id": 1,
                            "brand_id": 1,
                            "name": "vips_Event1",
                            "image": "",
                            "banner_image": "",
                            "text": "v",
                            "due": "2021-02-12T00:00:00",
                            "weekly_view": 'null',
                            "url": 'null'
                        },
                        {
                            "id": 2,
                            "created_date": "2021-07-11",
                            "update_date": "2021-07-21",
                            "category_id": 1,
                            "brand_id": 1,
                            "name": "vips_Event2",
                            "image": "",
                            "banner_image": "",
                            "text": "vv",
                            "due": "2010-02-12T00:00:00",
                            "weekly_view": 'null',
                            "url": 'null'
                        }
                    ],
                    "off_subscribe": [
                        "Yes",
                        "No"
                    ]
                }
            }
        )
    }

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'brand_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='int')
        }
    ), responses=response_schema_dict3)
    @action(detail=False, methods=['post'])
    def deadline(self, request):
        """
            브랜드 상세에서 해당 브랜드의 이벤트 목록

            # header
                - Authorization : jwt ey93..... [jwt token]
            # URL
                - POST /api/events/deadline/

        """
        data = JSONParser().parse(request)
        brand_id = data['brand_id']
        user_id = request.user.id
        subscribe = SubscribeEvent.objects.filter(user=user_id)
        now = datetime.datetime.now()
        # 하트순 정렬 하려면 _order_by로 못하고 하트인거랑 아닌거 나눠서 해야할듯
        off = Event.objects.filter(brand=brand_id, due__lte=now).order_by('-id')
        on = Event.objects.filter(brand=brand_id, due__gt=now).order_by('-id')
        on_subscribe = []
        off_subscribe = []
        for i in on:
            for j in subscribe:
                if i.id == j.event.id:
                    on_subscribe.append("Yes")
                    break
            else:
                on_subscribe.append("No")
        for i in off:
            for j in subscribe:
                if i.id == j.event.id:
                    off_subscribe.append("Yes")
                    break
            else:
                off_subscribe.append("No")
        off_event = off.values()
        on_event = on.values()
        return JsonResponse({'on_event': list(on_event),
                             'on_subscribe': on_subscribe,
                             'off_event': list(off_event),
                             'off_subscribe': off_subscribe}, status=200)

    response_schema_dict2 = {
        "200": openapi.Response(
            description="해당 카테고리 + 브랜드 필터링을 거친 모든 이벤트 목록과 좋아요 정보를 제공하는 API",
            examples={
                "application/json": {
                    "event": [
                        {
                            "id": 1,
                            "created_date": "2021-07-11",
                            "update_date": "2021-07-21",
                            "category_id": 1,
                            "brand_id": 1,
                            "name": "vips_Event1",
                            "image": "",
                            "banner_image": "",
                            "text": "v",
                            "due": "2021-02-12T00:00:00",
                            "weekly_view": 'null',
                            "url": 'null'
                        },
                        {
                            "id": 2,
                            "created_date": "2021-07-11",
                            "update_date": "2021-07-21",
                            "category_id": 1,
                            "brand_id": 1,
                            "name": "vips_Event2",
                            "image": "",
                            "banner_image": "",
                            "text": "vv",
                            "due": "2010-02-12T00:00:00",
                            "weekly_view": 'null',
                            "url": 'null'
                        }
                    ],
                    "subscribe": [
                        "Yes",
                        "No"
                    ]
                }
            }
        )
    }

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'category_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='int'),
            'brand_id': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_NUMBER),
                                       description='int')
        }
    ), responses=response_schema_dict2)
    @action(detail=False, methods=['post'])
    def main(self, request):
        """
            카테고리, 브랜드 별 이벤트 목록

            # header
                - Authorization : jwt ey93..... [jwt token]
            # URL
                - POST /api/events/main/

        """
        data = JSONParser().parse(request)
        category_id = data['category_id']
        user_id = request.user.id
        brand_id = data['brand_id']
        events = Event.objects.none()
        if len(brand_id) == 0:
            events = Event.objects.filter(category=category_id).order_by('-id')
        else:
            for i in brand_id:
                event = Event.objects.filter(brand=i, category=category_id).order_by('-id')
                events = events.union(event)

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

    response_schema_dict1 = {
        "200": openapi.Response(
            description="특정 이벤트의 상세 정보와 좋아요 정보를 제공하는 API",
            examples={
                "application/json": {
                    "event": [
                        {
                            "id": 1,
                            "created_date": "2021-07-11",
                            "update_date": "2021-07-21",
                            "category_id": 1,
                            "brand_id": 1,
                            "name": "vips_Event1",
                            "image": "",
                            "banner_image": "",
                            "text": "v",
                            "due": "2021-02-12T00:00:00",
                            "weekly_view": 'null',
                            "url": 'null'
                        }
                    ],
                    "subscribe": [
                        "Yes"
                    ]
                }
            }
        )
    }

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'event_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='int')
        }
    ), responses=response_schema_dict1)
    @action(detail=False, methods=['post'])
    def details(self, request):
        """
            이벤트 상세

            # header
                - Authorization : jwt ey93..... [jwt token]
            # URL
                - POST /api/events/details/

        """
        data = JSONParser().parse(request)
        event_id = data['event_id']
        user_id = request.user.id
        events = Event.objects.filter(id=event_id)
        events.update(view=events[0].view+1)
        subscribes = SubscribeEvent.objects.filter(user=user_id)
        subscribe = []
        for i in subscribes:
            if events[0].id == i.event.id:
                subscribe.append("Yes")
                break
        else:
            subscribe.append("No")
        event = events.values()
        return JsonResponse({'event': list(event),
                             'subscribe': subscribe}, status=200)

    @action(detail=False, methods=['post'])
    def test(self, request):
        test = ''+str(request.user.id)
        return JsonResponse({'result': test}, status=200)

'''
    # 알림 디비 자동화 오버라이딩 ( postman 으로 안쓰니 폐기 )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        #data = JSONParser().parse(request)
        brand_id = request.POST.get('brand', '')
        name = request.POST.get('name', '')
        subscribe = SubscribeBrand.objects.filter(brand=brand_id)
        #event = Event.objects.get(name=name)
        for i in subscribe:
            Notification.objects.create(user=User.objects.get(id=i.user.id))
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
'''