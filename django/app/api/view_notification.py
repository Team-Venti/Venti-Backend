# coding=utf-8
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .models import Event, Notification
from .serializer_notification import NotificationSerializer


class Notifications(APIView):
    """
        알림을 저장 하는 API ( 마감 알림 요청 )
        ---
        # 예시
            - POST /api/notifications/
        # parameters
            - "user" : 1 (유저 id)
            - "notice_type" : "end" (고정)
            - "event" : 1 (이벤트 id)
            - "url" : "www.naver.com" (이벤트 url) - NULL 가능
        # Responses
            - "user":
            - "notice_type":
            - "event":
            - "brand":
            - "url":
    """
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class NotificationUser(APIView):
    """
        특정 유저의 알림을 불러오는 API
        ---
        # 예시
            - POST /api/notifications/users/
        # parameters
            - "users" : 1 (유저 id)
        # Responses
            - result : [알림 목록]
    """
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        user = data['user']
        noti = Notification.objects.filter(user=user).order_by('-id')[:30]   # 30개까지 최신순 정렬
        result = noti.values()
        return JsonResponse({'result': list(result)}, status=200)
