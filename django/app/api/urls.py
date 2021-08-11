# coding=utf-8
from django.urls import path, include
from api import views
from .views import UserViewSet
from rest_framework.routers import DefaultRouter
# 기능 구현하고 import ( 밑에 router 연결도 해야함 )
# 현진
# from .view_login import ~ViewSet
# .view_join import ~ViewSet
# .view_mainpage import ~ViewSet
# 준기
from . import view_notification
from .view_brand import BrandViewSet
from .view_event import EventViewSet
from .view_subscribeEvent import SubscribeEventViewSet
from .view_subscribeBrand import SubscribeBrandViewSet, BrandLike
from .views_search import Search, GuestSearch
from .view_eventforyou import EventforyouView
from .view_weekly import Weekly, BannerWeekly, PagenationTest1, PagenationTest2
from .view_notification import *
from .view_guest import BrandMain, BrandDetail, EventMain, EventDetail, EventDeadline, BrandList
# 추가
# .view_notification import ~ViewSet
# 관리자 기능? 관련

# CBV
# urlpatterns = [
#     path('post/', views.PostList.as_view()),
#     path('post/<int:pk>', views.PostDetail.as_view())
#     ]

# ViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'events', EventViewSet)
# router.register(r'eventforyou', EventForYouViewSet)
router.register(r'myevents', SubscribeEventViewSet)
router.register(r'mybrands', SubscribeBrandViewSet)
# router.register(r'search', Search)    # post 용도로만

urlpatterns = [
    path('', include(router.urls)),
    # path('notifications/', Notifications.as_view()),
    path('notifications/users/', NotificationUser.as_view()),
    # path('noti/', view_notification.noti),
    path('guest/search/', GuestSearch.as_view()),
    path('search/', Search.as_view()),
    path('weekly/', BannerWeekly.as_view()),
    path('pagenations1/', PagenationTest1.as_view()),
    path('pagenations2/', PagenationTest2.as_view()),
    # path('weekly/', Weekly.as_view()), 배너 실시간 일때!
    path('eventforyou/', EventforyouView.as_view(),name = "eventforyou"),
    path('guest/brand_list/', BrandList.as_view()),
    path('guest/brand_main/', BrandMain.as_view()),
    path('guest/brand_detail/', BrandDetail.as_view()),
    path('guest/event_main/', EventMain.as_view()),
    path('guest/event_detail/', EventDetail.as_view()),
    path('guest/event_deadline/', EventDeadline.as_view()),
    path('guest/mybrands/', BrandLike.as_view())
]