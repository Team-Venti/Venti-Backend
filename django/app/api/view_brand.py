# coding=utf-8
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser

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
    """
        브랜드 목록을 불러오거나 저장/수정/삭제 하는 API
        ---
        # 예시
            - GET /api/brands/
            - GET /api/brands/?category=1
            - GET /api/brands/{id}

    """
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BrandFilter

    @action(detail=False, methods=['post'])
    def get_main(self, request):
        data = JSONParser().parse(request)
        category_id = data['category_id']
        user_id = data['user_id']
        brands = Brand.objects.filter(category=category_id)
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

