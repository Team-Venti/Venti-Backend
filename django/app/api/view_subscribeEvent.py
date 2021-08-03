# coding=utf-8
import datetime

from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser

from .models import SubscribeEvent, Event, User, Banner
from .serializer_subscribeEvent import SubscribeEventSerializer
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# 이벤트 좋아요 버튼, 마이브랜드_이벤트

'''
class SubscribeEventFilter(FilterSet):
    user = filters.NumberFilter(field_name="user")

    class Meta:
        model = SubscribeEvent
        fields = ['user']
'''

class SubscribeEventViewSet(viewsets.ModelViewSet):
    '''
        POST /api/myevents/ - 유저의 이벤트 좋아요 생성
        GET /api/myevents/users/ - 유저의 마이이벤트 목록
        POST /api/myevents/unlike/ - 유저의 이벤트 좋아요 취소
    '''
    serializer_class = SubscribeEventSerializer
    queryset = SubscribeEvent.objects.all()
    filter_backends = (DjangoFilterBackend,)
    # filterset_class = SubscribeEventFilter

    response_schema_dict3 = {
        "200": openapi.Response(
            description="유저의 이벤트 좋아요 생성하는 API",
            examples={
                "application/json": {
                    "message": "이벤트 좋아요 성공"
                }
            }
        )
    }

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'event_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='int')
        }
    ), responses=response_schema_dict3)
    def create(self, request, *args, **kwargs):
        """
            유저의 이벤트 좋아요

            # header
                - Authorization : jwt ey93..... [jwt token]
            # URL
                - POST /api/myevents/

        """
        data = JSONParser().parse(request)
        user_id = request.user.id
        event_id = data['event_id']
        event = Event.objects.get(id=event_id)
        SubscribeEvent.objects.create(user=User.objects.get(id=user_id),
                                      event=event)
        banner = Banner.objects.filter(name=event.brand.name)
        banner.update(count=banner[0].count + 1)
        return JsonResponse({"message": "이벤트 좋아요 성공"}, status=200)

    response_schema_dict2 = {
        "200": openapi.Response(
            description="유저의 이벤트 좋아요를 취소하는 API",
            examples={
                "application/json": {
                    "message": "이벤트 좋아요 취소"
                }
            }
        )
    }

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'event_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='int')
        }
    ), responses=response_schema_dict2)
    @action(detail=False, methods=['post'])
    def unlike(self, request):
        """
            유저의 이벤트 좋아요 취소

            # header
                - Authorization : jwt ey93..... [jwt token]
            # URL
                - POST /api/myevents/unlike/

        """
        data = JSONParser().parse(request)
        user_id = request.user.id
        event_id = data['event_id']
        event = Event.objects.get(id=event_id)
        banner = Banner.objects.filter(name=event.brand.name)
        banner.update(count=banner[0].count - 1)
        subscribe = SubscribeEvent.objects.filter(user=user_id, event=event_id)
        subscribe.delete()
        return JsonResponse({"message": "이벤트 좋아요 취소"}, status=200)

    response_schema_dict2 = {
        "200": openapi.Response(
            description="마이 벤티의 모든 좋아요 목록과 진행/마감 정보를 제공하는 API",
            examples={
                "application/json": {
                    "on_event": [
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
                            "due": "2021-12-12T00:00:00",
                            "weekly_view": 'null',
                            "url": 'null'
                        }
                    ],
                    "off_event": [
                        {
                            "id": 3,
                            "created_date": "2021-07-11",
                            "update_date": "2021-07-21",
                            "category_id": 2,
                            "brand_id": 3,
                            "name": "star_Event1",
                            "image": "",
                            "banner_image": "",
                            "text": "s1",
                            "due": "2019-02-12T00:00:00",
                            "weekly_view": 'null',
                            "url": 'null'
                        },
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
                    ]
                }
            }
        )
    }

    @swagger_auto_schema(responses=response_schema_dict2)
    @action(detail=False, methods=['get'])
    def users(self, request):
        """
            유저의 마이이벤트 목록을 불러오는 API

            # header
                - Authorization : jwt ey93..... [jwt token]
            # URL
                - GET /api/myevents/users/

        """
        user_id = request.user.id
        on_event = Event.objects.none()
        off_event = Event.objects.none()
        now = datetime.datetime.now()
        myevent = SubscribeEvent.objects.filter(user=user_id).order_by('-event__id')
        # for i in myevent: i.event의 id를 가진 event의 due, time 비교
        for i in myevent:
            on = Event.objects.filter(id=i.event.id, due__gt=now)
            off = Event.objects.filter(id=i.event.id, due__lte=now)
            on_event = on_event.union(on)
            off_event = off_event.union(off)

        onevent = on_event.values()
        offevent = off_event.values()
        return JsonResponse({'on_event': list(onevent),
                             'off_event': list(offevent)}, status=200)
