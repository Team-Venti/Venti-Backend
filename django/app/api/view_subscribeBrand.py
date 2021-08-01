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

# 브랜드 좋아요 버튼, 마이브랜드_브랜드


class SubscribeBrandFilter(FilterSet):
    user = filters.NumberFilter(field_name="user")

    class Meta:
        model = SubscribeBrand
        fields = ['user']


class SubscribeBrandViewSet(viewsets.ModelViewSet):
    """
        유저의 브랜드 구독 목록을 불러오거나 저장/삭제 하는 API
        ---
        # 예시
            - GET /api/mybrands/
            - POST /api/mybrands/
            - POST /api/mybrands/users/
            - DELETE /api/mybrands/{id}
    """
    serializer_class = SubscribeBrandSerializer
    queryset = SubscribeBrand.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SubscribeBrandFilter

    @action(detail=False, methods=['post'])
    def users(self, request):
        data = JSONParser().parse(request)
        user = data['user']
        my = SubscribeBrand.objects.filter(user=user)
        mybrand = my.values()
        return JsonResponse({'mybrand': list(mybrand)}, status=200)

# jwt말고 헤더로 로그인 하는법 필요
@permission_classes([IsAuthenticated])
class BrandLike(APIView):
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        user_id = data['user_id']
        brand_id = data['brand_id']
        for i in brand_id:
            SubscribeBrand.objects.create(user=User.objects.get(id=user_id), brand=Brand.objects.get(id=i))
        return JsonResponse({'status': "브랜드 구독 성공"}, status=200)
