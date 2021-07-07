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
class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # filter_backends = [DjangoFilterBackend]