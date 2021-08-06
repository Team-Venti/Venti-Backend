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
                        "id": 1,
                        "created_date": "2021-08-04",
                        "update_date": "2021-08-04",
                        "category_id": 1,
                        "brand_id": 1,
                        "name": "aalike",
                        "image": "event_logo/버거킹배너.jpeg",
                        "text": "dd",
                        "due": "2021-08-07T10:27:49",
                        "view": 2,
                        "url": "https://magazine.musinsa.com/index.php?m=news&cat=EVENT&uid=47461",
                        "d-day": 1,
                        "event_img_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/event_logo/버거킹배너.jpeg"
                    },
                    {
                        "id": 2,
                        "created_date": "2021-08-04",
                        "update_date": "2021-08-04",
                        "category_id": 1,
                        "brand_id": 1,
                        "name": "aaunlike",
                        "image": "event_logo/버거킹.png",
                        "text": "dd",
                        "due": "2021-08-07T10:28:05",
                        "view": 1,
                        "url": "http://event.com",
                        "d-day": 1,
                        "event_img_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/event_logo/버거킹.png"
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
            brand_name = Brand.objects.filter(id=each_event['brand_id'])
            each_event['brand_name'] = brand_name[0].name
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
                        "id": 1,
                        "created_date": "2021-08-04",
                        "update_date": "2021-08-04",
                        "category_id": 1,
                        "brand_id": 1,
                        "name": "aalike",
                        "image": "event_logo/버거킹배너.jpeg",
                        "text": "dd",
                        "due": "2021-08-07T10:27:49",
                        "view": 2,
                        "url": "https://magazine.musinsa.com/index.php?m=news&cat=EVENT&uid=47461",
                        "subs": "true",
                        "d-day": 1,
                        "event_img_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/event_logo/버거킹배너.jpeg"
                    },
                    {
                        "id": 2,
                        "created_date": "2021-08-04",
                        "update_date": "2021-08-04",
                        "category_id": 1,
                        "brand_id": 1,
                        "name": "aaunlike",
                        "image": "event_logo/버거킹.png",
                        "text": "dd",
                        "due": "2021-08-07T10:28:05",
                        "view": 1,
                        "url": "http://event.com",
                        "subs": "false",
                        "d-day": 1,
                        "event_img_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/event_logo/버거킹.png"
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
        event_list =[]
        for each_event in unique:
            brand_name = Brand.objects.filter(id=each_event['brand_id'])
            each_event['brand_name'] = brand_name[0].name
            each_event['event_img_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(each_event['image'])
            event_list.append(each_event)
        return Response({
            "events" : event_list
            # 'search_brand': list(brand.values())
        }, status=200) # list(result_set)