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


class SubscribeBrandFilter(FilterSet):
    user = filters.NumberFilter(field_name="user")

    class Meta:
        model = SubscribeBrand
        fields = ['user']


class SubscribeBrandViewSet(viewsets.ModelViewSet):
    '''
        POST /api/mybrands/ - 유저의 브랜드 구독 생성 ( { "user": , "brand": } )
        POST /api/mybrands/users/ - 유저의 마이브랜드 목록을 불러오는 API
        POST /api/guest/mybrand/ - 회원가입 할때 유저의 브랜드 구독 생성
    '''
    serializer_class = SubscribeBrandSerializer
    queryset = SubscribeBrand.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SubscribeBrandFilter

    response_schema_dict2 = {
        "200": openapi.Response(
            description="유저의 마이브랜드 목록을 불러오는 API",
            examples={
                "application/json": {
                    "mybrand": [
                        {
                            "id": 1,
                            "created_date": "2021-07-11",
                            "update_date": "2021-07-11",
                            "user_id": 2,
                            "brand_id": 1
                        },
                        {
                            "id": 2,
                            "created_date": "2021-07-11",
                            "update_date": "2021-07-11",
                            "user_id": 2,
                            "brand_id": 3
                        }
                    ]
                }
            }
        )
    }

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='int')
        }
    ), responses=response_schema_dict2)
    @action(detail=False, methods=['post'])
    def users(self, request):
        data = JSONParser().parse(request)
        user = data['user_id']
        my = SubscribeBrand.objects.filter(user=user)
        mybrand = my.values()
        return JsonResponse({'mybrand': list(mybrand)}, status=200)


@permission_classes([IsAuthenticated])
class BrandLike(APIView):
    response_schema_dict3 = {
        "200": openapi.Response(
            description="유저의 마이브랜드 목록을 불러오는 API",
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
            'user_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='int'),
            'brand_id': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_NUMBER),
                                       description='int')
        }
    ), responses=response_schema_dict3)
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        user_id = data['user_id']
        brand_id = data['brand_id']
        for i in brand_id:
            SubscribeBrand.objects.create(user=User.objects.get(id=user_id), brand=Brand.objects.get(id=i))
        return JsonResponse({'message': "브랜드 구독 성공"}, status=200)
