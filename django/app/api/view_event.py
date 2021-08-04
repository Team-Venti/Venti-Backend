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
import datetime
from .models import Event, Brand, SubscribeEvent, Notification, SubscribeBrand, User
from .serializer_event import EventSerializer, EventListSerializer
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
                            "id": 4,
                            "created_date": "2021-07-11",
                            "update_date": "2021-07-21",
                            "category_id": 3,
                            "brand_id": 4,
                            "name": "nike_Event1",
                            "image": "",
                            "text": "n1",
                            "due": "2030-02-12T00:00:00",
                            "view": 'null',
                            "url": 'null',
                            "subs": 'false',
                            "brand_name": "nike"
                        },
                        {
                            "id": 38,
                            "created_date": "2021-08-02",
                            "update_date": "2021-08-02",
                            "category_id": 3,
                            "brand_id": 4,
                            "name": "vips(nike_event)",
                            "image": "event_logo/KakaoTalk_20180520_163620948_cSBCjiS.jpg",
                            "text": "hi",
                            "due": "2021-10-01T00:00:00",
                            "view": "0000-00-00",
                            "url": "http://www.naver.com",
                            "subs": 'true',
                            "brand_name": "nike"
                        }
                    ],
                    "off_event": []
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
        on_event = []
        off_event = []
        now = datetime.datetime.now()
        subscribes = SubscribeEvent.objects.filter(user=user_id)
        events = Event.objects.filter(brand=brand_id)
        for each_event in events.values():
            brand = Brand.objects.get(id=each_event['brand_id'])
            # brand_name = each_event['brand'].name
            for each_sub in subscribes:
                if each_event['id'] == each_sub.event.id:
                    if each_event['due'] > now:
                        on_event.append(each_event)
                        on_event[-1]['subs'] = True
                        on_event[-1]['brand_name'] = brand.name
                    else:
                        off_event.append(each_event)
                        off_event[-1]['subs'] = True
                        off_event[-1]['brand_name'] = brand.name
                    break
            else:
                if each_event['due'] > now:
                    on_event.append(each_event)
                    on_event[-1]['subs'] = False
                    on_event[-1]['brand_name'] = brand.name
                else:
                    off_event.append(each_event)
                    off_event[-1]['subs'] = False
                    off_event[-1]['brand_name'] = brand.name

        return JsonResponse({"on_event": on_event,
                             "off_event": off_event}, status=200)

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
        data = JSONParser().parse(request)  # 아 D-1 이거 줘야한다...
        category_id = data['category_id']
        brand_id = data['brand_id']
        user_id = request.user.id
        subscribes = SubscribeEvent.objects.filter(user=user_id)
        now = datetime.datetime.now()
        event = []
        if len(brand_id) == 0:
            events = Event.objects.filter(category=category_id, due__gt=now).order_by('-id')
            for each_event in events.values():
                for each_sub in subscribes:
                    if each_sub.event.id == each_event['id']:
                        brand = Brand.objects.get(id=each_event['brand_id'])
                        event.append(each_event)
                        event[-1]['brand_name'] = brand.name
                        event[-1]['subs'] = True
                        break
                else:
                    brand = Brand.objects.get(id=each_event['brand_id'])
                    event.append(each_event)
                    event[-1]['brand_name'] = brand.name
                    event[-1]['subs'] = False
        else:
            for i in brand_id:
                events = Event.objects.filter(brand=i, category=category_id, due__gt=now).order_by('-id')
                for each_event in events.values():
                    for each_sub in subscribes:
                        if each_sub.event.id == each_event['id']:
                            brand = Brand.objects.get(id=each_event['brand_id'])
                            event.append(each_event)
                            event[-1]['brand_name'] = brand.name
                            event[-1]['subs'] = True
                            break
                    else:
                        brand = Brand.objects.get(id=each_event['brand_id'])
                        event.append(each_event)
                        event[-1]['brand_name'] = brand.name
                        event[-1]['subs'] = False

        return JsonResponse({'event': event}, status=200)

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
        event = []
        for each_event in events.values():
            for each_sub in subscribes:
                if each_sub.event.id == each_event['id']:
                    brand = Brand.objects.get(id=each_event['brand_id'])
                    event.append(each_event)
                    event[-1]['brand_name'] = brand.name
                    event[-1]['subs'] = True
                    break
            else:
                brand = Brand.objects.get(id=each_event['brand_id'])
                event.append(each_event)
                event[-1]['brand_name'] = brand.name
                event[-1]['subs'] = False

        return JsonResponse({'event': event}, status=200)

    # 테스트 코드
    @action(detail=False, methods=['post'])
    def test(self, request):
        data = JSONParser().parse(request)
        brand_id = data['brand_id']
        on_event = []
        off_event = []
        now = datetime.datetime.now()
        events = Event.objects.filter(brand=brand_id)
        for each_event in events.values():
            brand = Brand.objects.get(id=each_event['brand_id'])
            if each_event['due'] > now:
                on_event.append(each_event)
                on_event[-1]['brand_name'] = brand.name
            else:
                off_event.append(each_event)
                off_event[-1]['brand_name'] = brand.name

        return JsonResponse({"on_event": on_event,
                             "off_event": off_event}, status=200)

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