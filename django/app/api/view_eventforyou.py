# coding=utf-8
# from rest_framework import viewsets
import json
# from rest_framework_swagger import renderers
# from rest_framework.decorators import api_view, renderer_classes
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from .models import Event, SubscribeBrand,SubscribeEvent, Brand
from django.http import JsonResponse, HttpResponse
from .serializer_subscribeBrand import UseridSerializer
from rest_framework.parsers import JSONParser
# from api.utils import error_collections

#redoc
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# eventforyou
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
from drf_yasg.inspectors import SwaggerAutoSchema
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import datetime


response_schema_dict = {
    "200": openapi.Response(
        description="사용자가 좋아요 한 브랜드의 이벤트를 보여준다.",
        examples={
            "application/json": {
                "event": [
                    {
                        "id": 1,
                        "created_date": "2021-08-04T00:00:00",
                        "update_date": "2021-08-04T00:00:00",
                        "category_id": 1,
                        "brand_id": 1,
                        "name": "aalike",
                        "image": "event_logo/버거킹배너.jpeg",
                        "text": "dd",
                        "due": "2021-08-07T10:27:49",
                        "view": 2,
                        "url": "https://magazine.musinsa.com/index.php?m=news&cat=EVENT&uid=47461",
                        "brand_name": "aa",
                        "event_img_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/event_logo/버거킹배너.jpeg",
                        "d-day": 1,
                        "subs": "true"
                    },
                    {
                        "id": 2,
                        "created_date": "2021-08-04T00:00:00",
                        "update_date": "2021-08-04T00:00:00",
                        "category_id": 1,
                        "brand_id": 1,
                        "name": "aaunlike",
                        "image": "event_logo/버거킹.png",
                        "text": "dd",
                        "due": "2021-08-07T10:28:05",
                        "view": 1,
                        "url": "http://event.com",
                        "brand_name": "aa",
                        "event_img_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/event_logo/버거킹.png",
                        "d-day": 1,
                        "subs": "true"
                    }
                ]
            }
        }
    )
}

@permission_classes([IsAuthenticated])
@authentication_classes([JSONWebTokenAuthentication,])
class EventforyouView(APIView):
    '''
        회원일때 api
        POST /api/eventforyou/ - 메인페이지의 eventforyou
        비회원일때 api
        POST /api/guest/event_main/ - 메인페이지의 eventforyou
    '''
    model = Event, SubscribeBrand, SubscribeEvent
    # post : post 로 날라온 유저의 eventforyou 찾아주기

    @swagger_auto_schema(request_body= openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'category_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='int'),
        }
    ), responses=response_schema_dict)

    def post(self, request):
        events = []
        subevents = []
        user = request.user.id
        data = JSONParser().parse(request)  # 아 D-1 이거 줘야한다...
        category_id = data['category_id']
        # category_id = request.POST['category']
        subscribeevents = SubscribeEvent.objects.filter(user=user)
        for k in subscribeevents.values():
            subevents.append(k['event_id'])

        subscribebrands = SubscribeBrand.objects.filter(user=user)
        now = datetime.datetime.now()
        room = []
        for i in subscribebrands :
            brandname = i.brand.name
            eventforyou = Event.objects.filter(brand=i.brand,category = category_id, due__gt=now)
            for j in eventforyou.values() :
                j['brand_name'] = brandname
                j['event_img_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/'+str(j['image'])
                j['d-day'] = (j["due"] - now).days
                if j['id'] in subevents:
                    j['subs'] = True
                else:
                    j['subs'] = False
                events.append(j)
                room.append(j['id'])

        if (len(events) < 10):
            eventforyou = Event.objects.filter(category=category_id, due__gt=now).order_by("?")
            index = 10 - len(events)
            for j in eventforyou.values():
                brand = Brand.objects.filter(id = j['brand_id'])
                if j['id'] not in room:
                    index = index - 1
                    j['brand_name'] = brand[0].name
                    j['event_img_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(j['image'])
                    j['d-day'] = (j["due"] - now).days
                    if j['id'] in subevents:
                        j['subs'] = True
                    else:
                        j['subs'] = False
                    events.append(j)
                    if(index == 0):
                        break

        return JsonResponse({'event' : events}, status=200)
