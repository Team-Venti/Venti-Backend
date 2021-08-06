# coding=utf-8
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView

from .models import SubscribeBrand, Brand, User
from .serializer_subscribeBrand import SubscribeBrandSerializer
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# 브랜드 좋아요 버튼, 마이브랜드_브랜드

'''
class SubscribeBrandFilter(FilterSet):
    user = filters.NumberFilter(field_name="user")

    class Meta:
        model = SubscribeBrand
        fields = ['user']
'''

class SubscribeBrandViewSet(viewsets.ModelViewSet):
    '''
        POST /api/mybrands/ - 유저의 브랜드 구독 생성 ( { "user": , "brand": } )
        GET /api/mybrands/users/ - 유저의 마이브랜드 목록을 불러오는 API
        POST /api/guest/mybrand/ - 회원가입 할때 유저의 브랜드 구독 생성
    '''
    serializer_class = SubscribeBrandSerializer
    queryset = SubscribeBrand.objects.all()
    filter_backends = (DjangoFilterBackend,)
    # filterset_class = SubscribeBrandFilter

    response_schema_dict2 = {
        "200": openapi.Response(
            description="유저의 마이브랜드 목록을 불러오는 API",
            examples={
                "application/json": {
                    "mybrand": [
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
    @action(detail=False, methods=['get'])
    def users(self, request):
        """
            유저의 마이브랜드 목록을 불러오는 API

            # header
                - Authorization : jwt ey93..... [jwt token]
            # URL
                - GET /api/mybrands/users/

        """
        user = request.user.id
        my = SubscribeBrand.objects.filter(user=user).order_by('brand__category', 'brand__name')
        brands = Brand.objects.none()
        for i in my:
            brand = Brand.objects.filter(id=i.brand.id)
            brands = brands.union(brand)
        mybrand  = []
        for i in brands.values():
            i['brand_logo_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(i['image'])
            i['brand_banner_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(i['banner_image'])
            mybrand.append(i)
        return JsonResponse({'mybrand': mybrand}, status=200)

    response_schema_dict1 = {
        "200": openapi.Response(
            description="유저의 마이브랜드 구독을 취소하는 API",
            examples={
                "application/json": {
                    "message": "브랜드 구독 취소"
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
    @action(detail=False, methods=['post'])
    def unlike(self, request):
        """
            유저 브랜드 구독 취소

            # header
                - Authorization : jwt ey93..... [jwt token]
            # URL
                - POST /api/mybrands/unlike/

        """
        data = JSONParser().parse(request)
        user_id = request.user.id
        brand_id = data['brand_id']
        subscribe = SubscribeBrand.objects.filter(user=user_id, brand=brand_id)
        subscribe.delete()
        return JsonResponse({"message": "브랜드 구독 취소"}, status=200)

@permission_classes([IsAuthenticated])
class BrandLike(APIView):
    response_schema_dict3 = {
        "200": openapi.Response(
            description="브랜드 구독하는 API",
            examples={
                "application/json": {
                    "message": "브랜드 구독 성공"
                }
            }
        )
    }

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'brand_id': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_NUMBER),
                                       description='int')
        }
    ), responses=response_schema_dict3)
    def post(self, request, format=None):
        """
            브랜드 구독하는 API

            # header
                - Authorization : jwt ey93..... [jwt token]
            # URL
                - POST /api/guest/mybrands/

        """
        data = JSONParser().parse(request)
        user_id = request.user.id
        brand_id = data['brand_id']
        try:
            SubscribeBrand.objects.get(user=User.objects.get(id=user_id), brand=Brand.objects.get(id=brand_id))
            return JsonResponse({"message": "이미 구독한 브랜드입니다."}, status=200)
        except Exception as e:
            SubscribeBrand.objects.create(user=User.objects.get(id=user_id), brand=Brand.objects.get(id=brand_id))
            return JsonResponse({'message': "브랜드 구독 성공"}, status=200)
