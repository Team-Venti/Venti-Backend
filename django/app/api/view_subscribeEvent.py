# coding=utf-8
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser

from .models import SubscribeEvent
from .serializer_subscribeEvent import SubscribeEventSerializer
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend

# 이벤트 좋아요 버튼, 마이브랜드_이벤트


class SubscribeEventFilter(FilterSet):
    user = filters.NumberFilter(field_name="user")

    class Meta:
        model = SubscribeEvent
        fields = ['user']


class SubscribeEventViewSet(viewsets.ModelViewSet):
    """
        유저의 이벤트 좋아요 목록을 불러오거나 저장/삭제 하는 API
        ---
        # 예시
            - POST /api/myevents/
            - POST /api/myevents/users/
            - DELETE /api/myevents/{id}
    """
    serializer_class = SubscribeEventSerializer
    queryset = SubscribeEvent.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SubscribeEventFilter

    @action(detail=False, methods=['post'])
    def users(self, request):
        data = JSONParser().parse(request)
        user = data['user']
        myevent = SubscribeEvent.objects.filter(user=user)
        # for i in myevent: i.event의 id를 가진 event의 due, time 비교
        onevent = myevent.values()
        return JsonResponse({'onevent': list(onevent),
                             'offevent': list(onevent)}, status=200)
