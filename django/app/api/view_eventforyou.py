# coding=utf-8
# from rest_framework import viewsets
import json
# from rest_framework_swagger import renderers
# from rest_framework.decorators import api_view, renderer_classes

from rest_framework.views import APIView
from .models import Event, SubscribeBrand
from django.http import JsonResponse, HttpResponse
from .serializer_event import EventForYouSerializer
from rest_framework.parsers import JSONParser

# eventforyou
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
class EventforyouView(APIView):
    """
         메인페이지의 EventForYou 이벤트 목록을 불러오는 API
         ---
         # 내용
             - eventforyou : [EventForYou 이벤트 목록]
     """
    model = Event, SubscribeBrand
    # post : post 로 날라온 유저의 eventforyou 찾아주기
    def post(self, request):
        events = []
        # data = JSONParser().parse(request)
        # user id 가 있다
        # serializer = EventForYouSerializer(data= data)
        user = request.POST['user']
        subscribebrands = SubscribeBrand.objects.filter(user=user)
        for i in subscribebrands :
            eventforyou = Event.objects.filter(brand=i.brand)
            for j in eventforyou.values() :
                events.append(j)
        # 로그인 한다
        # return HttpResponse(events)
        # return JsonResponse({'eventforyou' : events})
        return JsonResponse({'eventforyou' : events})
    def get(self, request):
        user = request.GET['user']
        return HttpResponse(user)