# coding=utf-8
from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import Event, Brand, Banner
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

response_schema_dict = {
    "200": openapi.Response(
        description="인기 많은 브랜드 보여줌 (메인페이지 배너)",
        examples={
            "application/json": {
                "result": [
                    {
                        "id": 3,
                        "created_date": "2021-07-28",
                        "update_date": "2021-07-28",
                        "name": "nike",
                        "count": 4
                    },
                    {
                        "id": 1,
                        "created_date": "2021-07-28",
                        "update_date": "2021-07-28",
                        "name": "vips",
                        "count": 1
                    },
                    {
                        "id": 2,
                        "created_date": "2021-07-28",
                        "update_date": "2021-07-28",
                        "name": "김천",
                        "count": 0
                    },
                    {
                        "id": 4,
                        "created_date": "2021-07-28",
                        "update_date": "2021-07-28",
                        "name": "starbucks",
                        "count": 0
                    },
                    {
                        "id": 5,
                        "created_date": "2021-07-28",
                        "update_date": "2021-07-28",
                        "name": "momstouch",
                        "count": 0
                    }
                ]
            }
        }
    )
}

@permission_classes([AllowAny])
class Weekly(APIView):
    '''
        GET api/weekly/ - 메인페이지의 인기 배너
    '''

    @swagger_auto_schema(responses=response_schema_dict)
    def get(self, request, format=None):
        """
            메인페이지 인기 배너

            # URL
                - GET /api/weekly/

        """
        hot_brand = Banner.objects.all().order_by('-count')
        result = hot_brand.values()
        return JsonResponse({'result': list(result)}, status=200)
