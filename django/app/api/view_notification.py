# coding=utf-8
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .models import Event, Notification
from .serializer_notification import NotificationSerializer


class Notification(APIView):
    """
        알림을 저장 하는 API
        ---
        # 예시
            - GET /api/weekly/
        # parameters
            - No parameters
        # Responses
            - result : [알림 목록]
    """
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# 수정필요
class NotificationUser(APIView):
    """
        특정 유저의 알림을 불러오는 API
        ---
        # 예시
            - GET /api/weekly/
        # parameters
            - No parameters
        # Responses
            - result : [알림 목록]
    """
    def get(self, request):
        return HttpResponse(status=200)

    def post(self, request):
        data = JSONParser().parse(request)
        user = data['user']
        noti = Notification.objects.filter(user=user)   # .order_by('-id')[30]
        result = noti.values()
        return JsonResponse({'result': list(result)}, status=200)
