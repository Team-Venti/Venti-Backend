# coding=utf-8
# from rest_framework import viewsets
from django.views.generic import View
from .models import Event, SubscribeBrand
from .serializer_event import EventForYouSerializer
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend
#
# # 이벤트 메인, 이벤트 필터, 브랜드 상세, 이벤트 상세
#
#
# class EventForYouFilter(FilterSet):
#     class Meta:
#         model = Event
#         fields = ['brand']
#
#
# class EventForYouViewSet(viewsets.ModelViewSet):
#     user_brand = SubscribeEvent.objects.filter(user = user.id)
#     queryset = Event.objects.filter(brand = "")
#     serializer_class = EventForYouSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = EventForYouFilter

# coding=utf-8
# Create your views here.


# eventforyou
class eventforyouView(View):
    # post : post 로 날라온 유저의 eventforyou 찾아주기
    def post(self, request):
        if request.method == 'POST':
            events = []
            # user id 가 있다
            subscribebrands = SubscribeBrand.objects.filter(user=request.POST['user'])
            for i in subscribebrands :
                eventforyou = Event.objects.filter(brand=subscribebrands.name)
                events.append(eventforyou)
            # 로그인 한다
        return eventforyou
