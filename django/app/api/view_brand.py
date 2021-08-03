# coding=utf-8
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Brand, SubscribeBrand
from .serializer_brand import BrandSerializer
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend


# 브랜드


class BrandFilter(FilterSet):
    category = filters.NumberFilter(field_name="category")

    class Meta:
        model = Brand
        fields = ['category']


class BrandViewSet(viewsets.ModelViewSet):
    '''
    회원일때 api
    POST api/brands/main/ - 브랜드 메인
    POST api/brands/details/ - 브랜드 상세
    비회원일때 api
    POST api/guest/brand_main - 브랜드 메인
    POST api/guest/brand_detail/ - 브랜드 상세
    '''
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BrandFilter

    response_schema_dict2 = {
        "200": openapi.Response(
            description="해당 카테고리의 모든 브랜드 목록과 구독 정보를 제공하는 API",
            examples={
                "application/json": {
                    "brand": [
                        {
                            "id": 1,
                            "created_date": "2021-07-11",
                            "update_date": "2021-07-11",
                            "category_id": 1,
                            "image": "",
                            "name": "vips",
                            "text": "no1. stake house"
                        },
                        {
                            "id": 2,
                            "created_date": "2021-07-11",
                            "update_date": "2021-07-11",
                            "category_id": 1,
                            "image": "",
                            "name": "momstouch",
                            "text": "no1. hamburger"
                        }
                    ],
                    "subscribe": [
                        "Yes",
                        "No"
                    ]
                }
            }
        )
    }
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'category_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='int')
        }
    ), responses=response_schema_dict2)
    @action(detail=False, methods=['post'])
    def main(self, request):
        """
            카테고리 별 브랜드 목록

            # header
                - Authorization : jwt ey93..... [jwt token]
            # URL
                - POST /api/brands/main/

        """
        data = JSONParser().parse(request)
        category_id = data['category_id']
        user_id = request.user.id
        brands = Brand.objects.filter(category=category_id).order_by('name')
        subscribes = SubscribeBrand.objects.filter(user=user_id)
        subscribe = []
        for i in brands:
            for j in subscribes:
                if i.id == j.brand.id:
                    subscribe.append("Yes")
                    break
            else:
                subscribe.append("No")
        brand = brands.values()
        return JsonResponse({'brand': list(brand),
                             'subscribe': subscribe}, status=200)


    response_schema_dict1 = {
        "200": openapi.Response(
            description="브랜드를 클릭했을때 해당 브랜드의 상세 정보와 구독 정보를 제공하는 API",
            examples={
                "application/json": {
                    "brand": [
                        {
                            "id": 1,
                            "created_date": "2021-07-11",
                            "update_date": "2021-07-11",
                            "category_id": 1,
                            "image": "",
                            "name": "vips",
                            "text": "no1. stake house"
                        }
                    ],
                    "subscribe": [
                        "Yes"
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
    @action(detail=False, methods=['post'])
    def details(self, request):
        """
            브랜드 상세

            # header
                - Authorization : jwt ey93..... [jwt token]
            # URL
                - POST /api/brands/details/

        """
        data = JSONParser().parse(request)
        brand_id = data['brand_id']
        user_id = request.user.id
        brands = Brand.objects.filter(id=brand_id)
        subscribes = SubscribeBrand.objects.filter(user=user_id)
        subscribe = []
        for j in subscribes:
            if brands[0].id == j.brand.id:
                subscribe.append("Yes")
                break
        else:
            subscribe.append("No")
        brand = brands.values()
        return JsonResponse({'brand': list(brand),
                             'subscribe': subscribe}, status=200)