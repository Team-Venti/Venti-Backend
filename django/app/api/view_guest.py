# coding=utf-8
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
import datetime
from .models import Event, Brand
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import datetime

@permission_classes([AllowAny])
class BrandList(APIView):
    '''
    비회원일때 api
    GET api/guest/brand_list/ - 회원가입시 선호브랜드
    - request
    {
        x
    }
    '''
    response_schema_dict2 = {
        "200": openapi.Response(
            description="회원가입 시 선호브랜드에서 브랜드 목록 불러옴",
            examples={
                "application/json": {
                    "brand": [
                        {
                            "id": 1,
                            "created_date": "2021-08-04",
                            "update_date": "2021-08-04",
                            "category_id": 1,
                            "image": "brand_logo/무신사배너.jpeg",
                            "banner_image": "brand_banner/무신사페이.jpeg",
                            "name": "aa",
                            "text": "ddd",
                            "brand_logo_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_logo/무신사배너.jpeg",
                            "brand_banner_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_banner/무신사페이.jpeg"
                        },
                        {
                            "id": 2,
                            "created_date": "2021-08-04",
                            "update_date": "2021-08-04",
                            "category_id": 1,
                            "image": "brand_logo/버거킹.png",
                            "banner_image": "brand_banner/버거킹배너.jpeg",
                            "name": "bb",
                            "text": "bbb",
                            "brand_logo_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_logo/버거킹.png",
                            "brand_banner_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_banner/버거킹배너.jpeg"
                        }
                    ]
                }
            }
        )
    }
    @swagger_auto_schema(responses=response_schema_dict2)
    def get(self, request):
        """
            회원가입 선호브랜드 할때 브랜드 목록 불러옴

            # URL
                - GET /api/guest/brand_list/

        """
        brands = Brand.objects.filter(category=1).order_by('name')
        brand2 = Brand.objects.filter(category=2).order_by('name')
        brand3 = Brand.objects.filter(category=3).order_by('name')
        brands = brands.union(brand2)
        brands = brands.union(brand3)
        brand = brands.values()
        brand_list = []
        for i in brand:
            i['brand_logo_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(i['image'])
            i['brand_banner_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(i['banner_image'])
            brand_list.append(i)

        return JsonResponse({'brand': brand_list}, status=200)


@permission_classes([AllowAny])
class BrandMain(APIView):
    '''
    비회원일때 api
    POST api/guest/brand_main/ - 브랜드 메인
    - request
    {
        "category_id" : int (category id)
    }
    '''
    response_schema_dict3 = {
        "200": openapi.Response(
            description="카테고리 별 브랜드 목록",
            examples={
                "application/json": {
                    "brand": [
                        {
                            "id": 1,
                            "created_date": "2021-08-04",
                            "update_date": "2021-08-04",
                            "category_id": 1,
                            "image": "brand_logo/무신사배너.jpeg",
                            "banner_image": "brand_banner/무신사페이.jpeg",
                            "name": "aa",
                            "text": "ddd",
                            "brand_logo_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_logo/무신사배너.jpeg",
                            "brand_banner_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_banner/무신사페이.jpeg"
                        },
                        {
                            "id": 2,
                            "created_date": "2021-08-04",
                            "update_date": "2021-08-04",
                            "category_id": 1,
                            "image": "brand_logo/버거킹.png",
                            "banner_image": "brand_banner/버거킹배너.jpeg",
                            "name": "bb",
                            "text": "bbb",
                            "brand_logo_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_logo/버거킹.png",
                            "brand_banner_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_banner/버거킹배너.jpeg"
                        }
                    ]
                }
            }
        )
    }
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'category_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='int'),
        }
    ), responses=response_schema_dict3)
    def post(self, request, format=None):
        """
            (비회원일때) 카테고리 별 브랜드 목록

            # URL
                - POST /api/guest/brand_main/

        """
        data = JSONParser().parse(request)
        category_id = data['category_id']
        brands = Brand.objects.filter(category=category_id).order_by('name')
        brand = brands.values()
        brand_list = []
        for i in brand:
            i['brand_logo_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(i['image'])
            i['brand_banner_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(i['banner_image'])
            brand_list.append(i)
        return JsonResponse({'brand': brand_list}, status=200)


@permission_classes([AllowAny])
class BrandDetail(APIView):
    '''
    비회원일때 api
    POST api/guest/brand_detail/ - 브랜드 상세
    - request
    {
        "brand_id" : int (brand id)
    }
    '''
    response_schema_dict1 = {
        "200": openapi.Response(
            description="브랜드 상세",
            examples={
                "application/json": {
                    "brand": [
                        {
                            "id": 1,
                            "created_date": "2021-08-04",
                            "update_date": "2021-08-04",
                            "category_id": 1,
                            "image": "brand_logo/무신사배너.jpeg",
                            "banner_image": "brand_banner/무신사페이.jpeg",
                            "name": "aa",
                            "text": "ddd",
                            "brand_logo_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_logo/무신사배너.jpeg",
                            "brand_banner_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_banner/무신사페이.jpeg"
                        }
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
    ), responses=response_schema_dict1)
    def post(self, request, format=None):
        """
            (비회원일때) 브랜드 상세

            # URL
                - POST /api/guest/brand_detail/

        """
        data = JSONParser().parse(request)
        brand_id = data['brand_id']
        brands = Brand.objects.filter(id=brand_id)
        brand = brands.values()
        brand_list = []
        for i in brand:
            i['brand_logo_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(i['image'])
            i['brand_banner_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(i['banner_image'])
            brand_list.append(i)
        return JsonResponse({'brand': brand_list}, status=200)


@permission_classes([AllowAny])
class EventMain(APIView):
    '''
    비회원일때 api
    POST api/guest/event_main/ - 이벤트 메인, 비회원일때 eventforyou
    - request
    {
        "category_id" : int (category id),
        "brand_id" : int array (brand id)
    }
    '''
    response_schema_dict4 = {
        "200": openapi.Response(
            description="카테고리, 브랜드 별 이벤트 목록을 불러옴",
            examples={
                "application/json": {
                     "event": [
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
                            "event_img_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/event_logo/버거킹.png",
                            "brand_name": "aa",
                            "d-day": 1
                        },
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
                            "view": 0,
                            "url": "https://magazine.musinsa.com/index.php?m=news&cat=EVENT&uid=47461",
                            "event_img_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/event_logo/버거킹배너.jpeg",
                            "brand_name": "aa",
                            "d-day": 1
                        }
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
    ), responses=response_schema_dict4)
    def post(self, request, format=None):
        """
            (비회원일때) 카테고리, 브랜드 별 이벤트 목록 and (비회원일때) 메인페이지의 eventforyou

            # URL
                - POST /api/guest/event_main/

        """
        data = JSONParser().parse(request)
        category_id = data['category_id']
        brand_id = data['brand_id']
        now = datetime.datetime.now()
        event = []
        if len(brand_id) == 0:
            events = Event.objects.filter(category=category_id, due__gt=now).order_by('-id')
            for each in events.values():
                each['event_img_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(each['image'])
                brand = Brand.objects.get(id=each['brand_id'])
                ev = Event.objects.get(id=each['id'])
                event.append(each)
                event[-1]['brand_name'] = brand.name
                event[-1]['d-day'] = (ev.due - now).days
        else:
            for i in brand_id:
                events = Event.objects.filter(brand=i, category=category_id, due__gt=now).order_by('-id')
                for each in events.values():
                    each['event_img_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(each['image'])
                    brand = Brand.objects.get(id=each['brand_id'])
                    ev = Event.objects.get(id=each['id'])
                    event.append(each)
                    event[-1]['brand_name'] = brand.name
                    event[-1]['d-day'] = (ev.due - now).days

        return JsonResponse({'event': event}, status=200)


@permission_classes([AllowAny])
class EventDetail(APIView):
    '''
    비회원일때 api
    POST api/guest/event_detail/ - 이벤트 상세
    - request
    {
        "event_id" : int (event id)
    }
    '''
    response_schema_dict5 = {
        "200": openapi.Response(
            description="이벤트 상세",
            examples={
                "application/json": {
                    "event": [
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
                            "view": 1,
                            "url": "https://magazine.musinsa.com/index.php?m=news&cat=EVENT&uid=47461",
                            "event_img_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/event_logo/버거킹배너.jpeg",
                            "brand_name": "aa"
                        }
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
    ), responses=response_schema_dict5)
    def post(self, request, format=None):
        """
            (비회원일때) 이벤트 상세

            # URL
                - POST /api/guest/event_detail/

        """
        data = JSONParser().parse(request)
        event_id = data['event_id']
        events = Event.objects.filter(id=event_id)
        events.update(view=events[0].view+1)
        event = []
        for each_event in events.values():
            each_event['event_img_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(each_event['image'])
            brand = Brand.objects.get(id=each_event['brand_id'])
            event.append(each_event)
            event[-1]['brand_name'] = brand.name

        return JsonResponse({'event': event}, status=200)


@permission_classes([AllowAny])
class EventDeadline(APIView):
    '''
    비회원일때 api
    POST api/guest/event_deadline/ - 브랜드 상세 눌렀을때 밑에 이벤트들
    - request
    {
        "brand_id" : int (brand id)
    }
    '''
    response_schema_dict6 = {
        "200": openapi.Response(
            description="브랜드 상세에서 해당 브랜드의 이벤트 목록을 불러옴",
            examples={
                "application/json": {
                    "on_event": [
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
                            "view": 1,
                            "url": "https://magazine.musinsa.com/index.php?m=news&cat=EVENT&uid=47461",
                            "event_img_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/event_logo/버거킹배너.jpeg",
                            "brand_name": "aa"
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
                            "event_img_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/event_logo/버거킹.png",
                            "brand_name": "aa"
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
    ), responses=response_schema_dict6)
    def post(self, request, format=None):
        """
            (비회원일때) 브랜드 상세에서 해당 브랜드의 이벤트 목록

            # URL
                - POST /api/guest/event_deadline/

        """
        data = JSONParser().parse(request)
        brand_id = data['brand_id']
        on_event = []
        off_event = []
        now = datetime.datetime.now()
        events = Event.objects.filter(brand=brand_id)
        for each_event in events.values():
            each_event['event_img_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(each_event['image'])
            brand = Brand.objects.get(id=each_event['brand_id'])
            if each_event['due'] > now:
                on_event.append(each_event)
                on_event[-1]['brand_name'] = brand.name
            else:
                off_event.append(each_event)
                off_event[-1]['brand_name'] = brand.name

        return JsonResponse({"on_event": on_event,
                             "off_event": off_event}, status=200)