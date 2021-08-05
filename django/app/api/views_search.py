# coding=utf-8
from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import Event, Brand, SubscribeEvent
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
import datetime

response_schema_dict = {
    "200": openapi.Response(
        description="검색 결과를 보여준다.",
        examples={
            "application/json": {
            "events": [
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
                        "d-day": 56
                    },
                    {
                        "id": 1,
                        "created_date": "2021-07-11",
                        "update_date": "2021-07-21",
                        "category_id": 1,
                        "brand_id": 1,
                        "name": "vips_Event1",
                        "image": "",
                        "text": "v",
                        "due": "2021-08-08T00:00:00",
                        "view": 'null',
                        "url": 'null',
                        "d-day": 2
                    },
                    {
                        "id": 2,
                        "created_date": "2021-07-11",
                        "update_date": "2021-07-21",
                        "category_id": 1,
                        "brand_id": 1,
                        "name": "vips_Event2",
                        "image": "",
                        "text": "vv",
                        "due": "2010-08-07T00:00:00",
                        "view": 'null',
                        "url": 'null',
                        "d-day": 1
                    }
                ]
            }
        }
    )
}
@permission_classes([AllowAny])
class GuestSearch(APIView):
    '''
        검색
        GET /api/guest/search/?search=vips - 검색
    '''

    @swagger_auto_schema(responses=response_schema_dict)
    def get(self, request):
        """
            (비회원) 검색 결과

            # URL
                - GET /api/guest/search/?search=vips

        """
        name = request.GET['search']
        now = datetime.datetime.now()
        event = Event.objects.filter(name__contains=name, due__gt=now)
        brand = Brand.objects.filter(name__contains=name)
        events = []
        for i in event.values():
            ev = Event.objects.get(id=i['id'])
            events.append(i)
            events[-1]['d-day'] = (ev.due - now).days

        for i in brand:
            event_inbrand = Event.objects.filter(brand=i.id, due__gt=now)
            for j in event_inbrand.values():
                ev = Event.objects.get(id=j['id'])
                events.append(j)
                events[-1]['d-day'] = (ev.due - now).days

        # 중복 제거
        unique = { each['name'] : each for each in events }.values()
        event_list = []
        for each_event in unique:
            each_event['event_img_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(each_event['image'])
            event_list.append(each_event)

        return Response({
            "events" : event_list
        }, status=200) # list(result_set)



response_schema_dict2 = {
    "200": openapi.Response(
        description="검색 결과를 보여준다.",
        examples={
            "application/json": {
                "events": [
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
                            "d-day": 3112
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
                            "d-day": 56
                        }
                    ]
            }
        }
    )
}
class Search(APIView):
    '''
        검색
        GET /api/search/?search=vips - 검색
    '''

    @swagger_auto_schema(responses=response_schema_dict2)
    def get(self, request):
        """
            (회원) 검색 결과

            # header
                - Authorization : jwt ey93..... [jwt token]
            # URL
                - GET /api/search/?search=vips

        """
        name = request.GET['search']
        user_id = request.user.id
        now = datetime.datetime.now()
        event = Event.objects.filter(name__contains=name, due__gt=now)
        brand = Brand.objects.filter(name__contains=name)
        subscribe = SubscribeEvent.objects.filter(user=user_id)
        events = []
        for i in event.values():
            ev = Event.objects.get(id=i['id'])
            events.append(i)
            for each_subs in subscribe:
                if each_subs.event.id == i['id']:
                    events[-1]['subs'] = True
                    break
            else:
                events[-1]['subs'] = False
            events[-1]['d-day'] = (ev.due - now).days

        for i in brand:
            event_inbrand = Event.objects.filter(brand=i.id, due__gt=now)
            for j in event_inbrand.values():
                ev = Event.objects.get(id=j['id'])
                events.append(j)
                for each_subs in subscribe:
                    if each_subs.event.id == j['id']:
                        events[-1]['subs'] = True
                        break
                else:
                    events[-1]['subs'] = False
                events[-1]['d-day'] = (ev.due - now).days

        # 중복 제거
        unique = { each['name'] : each for each in events }.values()

        return Response({
            "events" : unique
            # 'search_brand': list(brand.values())
        }, status=200) # list(result_set)