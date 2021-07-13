from rest_framework import viewsets
from .models import SubscribeBrand
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
            - GET /api/mybrands/?user=1
            - POST /api/mybrands/
            - DELETE /api/mybrands/{id}
        # parameter
            - user : 어떤 유저가 구독 했는지 (Foreign Key)
            - brand : 어떤 브랜드를 구독 했는지 (Foreign Key)
    """
    serializer_class = SubscribeBrandSerializer
    queryset = SubscribeBrand.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SubscribeBrandFilter
