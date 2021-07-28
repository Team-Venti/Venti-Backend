# coding=utf-8
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Event, Brand, Banner
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

response_schema_dict = {
    "200": openapi.Response(
        description="인기 많은 이벤트 보여줌",
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


class Weekly(APIView):
    """
        인기 이벤트를 불러오거나 저장/수정/삭제 하는 API
        ---
        # 예시
            - GET /api/weekly/
        # parameters
            - No parameters
        # Responses
            - result : [인기 이벤트 목록]
    """

    def get(self, request, format=None):
        hot_brand = Banner.objects.all().order_by('-count')
        result = hot_brand.values()
        return JsonResponse({'result': list(result)}, status=200)
