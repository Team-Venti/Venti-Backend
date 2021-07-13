from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from .models import Event, Brand
from .serializer_search import SearchSerializer
from .serializer_brand import BrandSerializer
from .serializer_event import EventSerializer
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend


# 검색 - 미완


class Search(APIView):
    """
        검색한 브랜드/이벤트 목록을 불러오는 API
        ---
        # 예시
            - GET /api/search/?name=vips
        # parameter
            - search_event: [검색한 이벤트 목록]
            - search_brand: [검색한 브랜드 목록]
    """
    def get(self, request, format=None):
        name = request.GET['name']
        event = Event.objects.filter(name__contains=name)
        brand = Brand.objects.filter(name__contains=name)

        return JsonResponse({
            'search_event': list(event.values()),
            'search_brand': list(brand.values())
            }, status=200) # list(result_set)
