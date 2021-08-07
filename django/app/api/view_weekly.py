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
# 실시간으로 배너할때
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
        hot_brand = Brand.objects.all().order_by('-view')
        results = hot_brand.values()
        result_list = []
        for result in results :
            result['brand_logo_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(result['image'])
            result['brand_banner_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(result['banner_image'])
            result_list.append(result)

        return JsonResponse({'result': result_list}, status=200)


response_schema_dict2 = {
    "200": openapi.Response(
        description="인기 많은 브랜드 보여줌 (메인페이지 배너)",
        examples={
            "application/json": {
                "result": [
                    {
                        "id": 14,
                        "created_date": "2021-08-07T21:36:22.470",
                        "update_date": "2021-08-07T21:36:22.470",
                        "name": "test2",
                        "brand_id": 2,
                        "view": 4,
                        "brand_logo_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_logo/KakaoTalk_20180520_163620948_6hmc23u.jpg",
                        "brand_banner_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_banner/KakaoTalk_20180520_163620948_DTDMbR1.jpg"
                    },
                    {
                        "id": 13,
                        "created_date": "2021-08-07T21:36:22.459",
                        "update_date": "2021-08-07T21:36:22.459",
                        "name": "test3",
                        "brand_id": 3,
                        "view": 1,
                        "brand_logo_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_logo/KakaoTalk_20180520_163620948_ti0Y1Ci.jpg",
                        "brand_banner_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_banner/KakaoTalk_20180520_163620948_kpPdfgK.jpg"
                    },
                    {
                        "id": 15,
                        "created_date": "2021-08-07T21:36:22.476",
                        "update_date": "2021-08-07T21:36:22.476",
                        "name": "test1",
                        "brand_id": 1,
                        "view": 0,
                        "brand_logo_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_logo/KakaoTalk_20180520_163620948_ohSVrqW.jpg",
                        "brand_banner_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_banner/KakaoTalk_20180520_163620948_hwMIF57.jpg"
                    }
                ]
            }
        }
    )
}
#수작업 배너
@permission_classes([AllowAny])
class BannerWeekly(APIView):
    @swagger_auto_schema(responses=response_schema_dict2)
    def get(self, request):
        """
            메인페이지 인기 배너

            # URL
                - GET /api/weekly/

        """
        hot_brand = Banner.objects.all().order_by('-view')
        results = hot_brand.values()
        result = []
        for each in results:
            each['brand_logo_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(Brand.objects.get(id=each['brand_id']).image)
            each['brand_banner_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(Brand.objects.get(id=each['brand_id']).banner_image)
            result.append(each)

        return JsonResponse({'result': result}, status=200)
