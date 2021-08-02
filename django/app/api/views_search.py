# coding=utf-8
from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import Event, Brand
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
response_schema_dict = {
    "200": openapi.Response(
        description="검색 결과를 보여준다.",
        examples={
            "application/json": {
                    "search_event": [
                        {
                            "id": 1,
                            "created_date": "2021-07-11",
                            "update_date": "2021-07-11",
                            "category_id": 1,
                            "brand_id": 1,
                            "name": "vips_Event1",
                            "image": "",
                            "banner_image": "",
                            "text": "v",
                            "due": "2021-07-21",
                            "weekly_view": 4,
                            "url": "www.naver.com"
                        },
                        {
                            "id": 2,
                            "created_date": "2021-07-11",
                            "update_date": "2021-07-11",
                            "category_id": 1,
                            "brand_id": 1,
                            "name": "vips_Event2",
                            "image": "",
                            "banner_image": "",
                            "text": "vv",
                            "due": "2021-07-21",
                            "weekly_view": 3,
                            "url": "www.naver.com"
                        }
                    ],
                    "search_brand": [
                        {
                            "id": 1,
                            "created_date": "2021-07-11",
                            "update_date": "2021-07-11",
                            "category_id": 1,
                            "image": "",
                            "name": "vips",
                            "text": "no1. stake house"
                        }
                    ]
            }
        }
    )
}

@permission_classes([AllowAny])
class Search(APIView):
    '''
        검색
        GET /api/search/?search=vips - 검색
    '''
    def get(self, request):
        name = request.GET['search']
        event = Event.objects.filter(name__contains=name)
        brand = Brand.objects.filter(name__contains=name)
        events = []
        for i in event.values():
            events.append(i)

        for i in brand:
            event_inbrand = Event.objects.filter(brand=i.id)
            for j in event_inbrand.values():
                events.append(j)

        # 중복 제거
        unique = { each['name'] : each for each in events }.values()

        return Response({
            "events" : unique
            # 'search_brand': list(brand.values())
        }, status=200) # list(result_set)
