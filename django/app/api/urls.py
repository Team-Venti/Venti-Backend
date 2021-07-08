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
# .view_brand import ~ViewSet
# .view_event import ~ViewSet
# .view_mypage import ~ViewSet
# .view_login import ~ViewSet
# 추가
# .view_notification import ~ViewSet
# admin 관련

# CBV
# urlpatterns = [
#     path('post/', views.PostList.as_view()),
#     path('post/<int:pk>', views.PostDetail.as_view())
#     ]

# ViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet)
# router.register()
urlpatterns = [
    path('', include(router.urls)),
]