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
                "events": [
                    {
                        "id": 1,
                        "created_date": "2021-07-11",
                        "update_date": "2021-07-21",
                        "category_id": 1,
                        "brand_id": 1,
                        "name": "vips_Event1",
                        "image": "",
                        "text": "v",
                        "due": "2021-02-12T00:00:00",
                        "view": 'null',
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
                        "text": "vv",
                        "due": "2010-02-12T00:00:00",
                        "view": 'null',
                        "url": 'null'
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

    @swagger_auto_schema(responses=response_schema_dict)
    def get(self, request):
        """
            검색 결과

            # URL
                - GET /api/search/

        """
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
        event_list = []
        for each_event in unique:
            each_event['event_img_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(each_event['image'])
            event_list.append(each_event)

        return Response({
            "events" : event_list
        }, status=200) # list(result_set)
