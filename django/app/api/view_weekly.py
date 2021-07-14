# coding=utf-8
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from .models import Event, Brand
from .serializer_search import SearchSerializer


class Weekly(APIView):
    """
        인기 이벤트를 불러오거나 저장/수정/삭제 하는 API
        ---
        # 예시
            - GET /api/weekly/
        # parameter
            - result : [인기 이벤트 목록]
    """

    def get(self, request, format=None):
        hot_event = Event.objects.all().order_by('-weekly_view')
        result = hot_event.values()
        return JsonResponse({'result': list(result)}, status=200)
