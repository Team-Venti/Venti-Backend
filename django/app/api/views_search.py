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
        브랜드 목록을 불러오거나 저장/수정/삭제 하는 API
        ---
        # 내용
            - 미정
    """
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = SearchSerializer(data=data)    # 수정해야함
        print(serializer)
        return JsonResponse(serializer.errors,safe=False)
