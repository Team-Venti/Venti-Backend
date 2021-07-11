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
from .view_brand import BrandViewSet, BrandSubsViewSet
from .view_event import EventViewSet, EventSubsViewSet
# .view_mypage import ~ViewSet
# .view_search

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
router.register(r'brandsubs', BrandSubsViewSet)
router.register(r'events', EventViewSet)
router.register(r'eventsubs', EventSubsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]