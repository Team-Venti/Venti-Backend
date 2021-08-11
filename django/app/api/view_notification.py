# coding=utf-8
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .models import Event, Notification
from .serializer_notification import NotificationSerializer
from django.views.decorators.csrf import csrf_exempt
from background_task import background
from .models import *
from rest_framework.decorators import authentication_classes, permission_classes
from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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

    # 이거는 프엔에서 마감시간때 post 해서 알람디비 채워주는건데 안될것같으면 지워도 될듯 ( url 빼버림 )
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

response_schema_dict2 = {
    "200": openapi.Response(
        description="유저의 알림 목록을 제공하는 API",
        examples={
            "application/json": {
                "result": [
                    {
                        "id": 2,
                        "created_date": "2021-08-05",
                        "update_date": "2021-08-05",
                        "user_id": 1,
                        "event_id": 3,
                        "brand_id": 2,
                        "notice_type": "end12",
                        "url": "https://www.nike.com/kr/ko_kr/c/nike-membership",
                        "brand_name": "bb",
                        "event_name": "bblike",
                        "brand_img": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_logo/버거킹.png",
                        "d-day": 0,
                        "noti_time": 11
                    }
                ]
            }
        }
    )
}


class NotificationUser(APIView):
    '''
        GET /api/notifications/users/ - 특정 유저의 알림을 불러옴
    '''

    @swagger_auto_schema(responses=response_schema_dict2)
    def get(self, request, format=None):
        """
            유저의 알림 목록을 불러오는 API

            # header
                - Authorization : jwt ey93..... [jwt token]
            # URL
                - GET /api/notifications/users/

        """
        user = request.user.id
        noti = Notification.objects.filter(user=user).order_by('-id')[:30]  # 30개까지 최신순 정렬
        result = []
        now = datetime.now()
        for i in noti.values():
            brand = Brand.objects.filter(id=i['brand_id'])
            event = Event.objects.filter(id=i['event_id'])
            i['brand_name'] = brand[0].name
            i['event_name'] = event[0].name
            i['brand_img'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(brand[0].image)
            if i['notice_type'] == "end12":
                i['d-day'] = 0
            if i['notice_type'] == "end24":
                i['d-day'] = 1
            if i['notice_type'] == "end48":
                i['d-day'] = 2

            if (now - i['created_date']).days == 0 :
                if(now - i['created_date']).seconds < 3600 :
                    i['noti_time'] = str((now - i['created_date']).seconds//60)+'분 전'
                else:
                    i['noti_time'] = str((now - i['created_date']).seconds // 3600) + '시간 전'
            else :
                i['noti_time'] = str((now - i['created_date']).days) + '일 전'
            result.append(i)

        user = User.objects.filter(id=request.user.id)
        user.update(noti_state=False)
        return JsonResponse({'result': result}, status=200)

