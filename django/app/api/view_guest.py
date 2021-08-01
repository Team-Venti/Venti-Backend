# coding=utf-8
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
import datetime
from .models import Event, Brand


@permission_classes([AllowAny])
class BrandList(APIView):
    def get(self, request):
        brands = Brand.objects.filter(category=1).order_by('name')
        brand2 = Brand.objects.filter(category=2).order_by('name')
        brand3 = Brand.objects.filter(category=3).order_by('name')
        brands = brands.union(brand2)
        brands = brands.union(brand3)
        brand = brands.values()
        return JsonResponse({'brand': list(brand)}, status=200)


@permission_classes([AllowAny])
class BrandMain(APIView):
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        category_id = data['category_id']
        brands = Brand.objects.filter(category=category_id)
        brand = brands.values()
        return JsonResponse({'brand': list(brand)}, status=200)


@permission_classes([AllowAny])
class BrandDetail(APIView):
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        brand_id = data['brand_id']
        brands = Brand.objects.filter(id=brand_id)
        brand = brands.values()
        return JsonResponse({'brand': list(brand)}, status=200)


@permission_classes([AllowAny])
class EventMain(APIView):
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        category_id = data['category_id']
        brand_id = data['brand_id']
        events = Event.objects.none()
        if len(brand_id) == 0:
            events = Event.objects.filter(category=category_id)
        else:
            for i in brand_id:
                event = Event.objects.filter(brand=i, category=category_id)
                events = events.union(event)

        event = events.values()
        return JsonResponse({'event': list(event)}, status=200)


@permission_classes([AllowAny])
class EventDetail(APIView):
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        event_id = data['event_id']
        events = Event.objects.filter(id=event_id)
        event = events.values()
        return JsonResponse({'event': list(event)}, status=200)


@permission_classes([AllowAny])
class EventDeadline(APIView):
        def post(self, request, format=None):
            data = JSONParser().parse(request)
            brand_id = data['brand_id']
            now = datetime.datetime.now()
            off = Event.objects.filter(brand=brand_id, due__lte=now)
            on = Event.objects.filter(brand=brand_id, due__gt=now)
            off_event = off.values()
            on_event = on.values()
            return JsonResponse({'on_event': list(on_event),
                                 'off_event': list(off_event)}, status=200)