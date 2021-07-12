from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from .models import Event, Brand
from .serializer_search import SearchSerializer


# 임시니까 다 갈아엎으세용
class Weekly(APIView):
    """
        주간 인기 이벤트를 불러오거나 저장/수정/삭제 하는 API
        ---
        # 내용
            - 미정
    """

    def post(self, request, format=None):
        data = JSONParser().parse(request)
