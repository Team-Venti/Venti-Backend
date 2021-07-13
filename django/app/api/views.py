# coding=utf-8
from django.shortcuts import render
from rest_framework import status, mixins

from .models import User
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from django.http import HttpResponse
from django.views import View
# FBV
from rest_framework.decorators import api_view
from rest_framework.response import Response
# CBV
from .serializers import UserSerializer
from rest_framework.views import APIView
# ViewSet
from rest_framework import viewsets
# Filter
from django_filters.rest_framework import FilterSet, filters, DjangoFilterBackend
# Permission
from rest_framework import permissions


# Create your views here.

# ViewSet으로 class
class UserViewSet(viewsets.ModelViewSet):
    """
        유저 목록을 불러오거나 저장/수정/삭제 하는 API
        ---
        # 예시
            - GET /api/user/
            - POST /api/user/
            - DELETE /api/user/{id}
        # parameter
            - username : 유저의 아이디
            - nickname : 유저의 닉네임
            - password : 유저의 패스워드
            - email : 유저의 이메일
            - gender : 유저의 성별
            - birth : 유저의 생일
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # filter_backends = [DjangoFilterBackend]
