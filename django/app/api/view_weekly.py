# coding=utf-8
from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import Event, Brand, Banner, SubscribeEvent
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import datetime

response_schema_dict = {
    "200": openapi.Response(
        description="인기 많은 브랜드 보여줌 (메인페이지 배너)",
        examples={
            "application/json": {
                "result": [
                    {
                        "id": 3,
                        "created_date": "2021-07-28",
                        "update_date": "2021-07-28",
                        "name": "nike",
                        "count": 4
                    },
                    {
                        "id": 1,
                        "created_date": "2021-07-28",
                        "update_date": "2021-07-28",
                        "name": "vips",
                        "count": 1
                    },
                    {
                        "id": 2,
                        "created_date": "2021-07-28",
                        "update_date": "2021-07-28",
                        "name": "김천",
                        "count": 0
                    },
                    {
                        "id": 4,
                        "created_date": "2021-07-28",
                        "update_date": "2021-07-28",
                        "name": "starbucks",
                        "count": 0
                    },
                    {
                        "id": 5,
                        "created_date": "2021-07-28",
                        "update_date": "2021-07-28",
                        "name": "momstouch",
                        "count": 0
                    }
                ]
            }
        }
    )
}
# 실시간으로 배너할때
@permission_classes([AllowAny])
class Weekly(APIView):
    '''
        GET api/weekly/ - 메인페이지의 인기 배너
    '''

    @swagger_auto_schema(responses=response_schema_dict)
    def get(self, request, format=None):
        """
            메인페이지 인기 배너

            # URL
                - GET /api/weekly/

        """
        hot_brand = Brand.objects.all().order_by('-view')
        results = hot_brand.values()
        result_list = []
        for result in results :
            result['brand_logo_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(result['image'])
            result['brand_banner_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(result['banner_image'])
            result_list.append(result)

        return JsonResponse({'result': result_list}, status=200)


response_schema_dict2 = {
    "200": openapi.Response(
        description="인기 많은 브랜드 보여줌 (메인페이지 배너)",
        examples={
            "application/json": {
                "result": [
                    {
                        "id": 14,
                        "created_date": "2021-08-07T21:36:22.470",
                        "update_date": "2021-08-07T21:36:22.470",
                        "name": "test2",
                        "brand_id": 2,
                        "view": 4,
                        "brand_logo_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_logo/KakaoTalk_20180520_163620948_6hmc23u.jpg",
                        "brand_banner_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_banner/KakaoTalk_20180520_163620948_DTDMbR1.jpg"
                    },
                    {
                        "id": 13,
                        "created_date": "2021-08-07T21:36:22.459",
                        "update_date": "2021-08-07T21:36:22.459",
                        "name": "test3",
                        "brand_id": 3,
                        "view": 1,
                        "brand_logo_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_logo/KakaoTalk_20180520_163620948_ti0Y1Ci.jpg",
                        "brand_banner_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_banner/KakaoTalk_20180520_163620948_kpPdfgK.jpg"
                    },
                    {
                        "id": 15,
                        "created_date": "2021-08-07T21:36:22.476",
                        "update_date": "2021-08-07T21:36:22.476",
                        "name": "test1",
                        "brand_id": 1,
                        "view": 0,
                        "brand_logo_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_logo/KakaoTalk_20180520_163620948_ohSVrqW.jpg",
                        "brand_banner_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_banner/KakaoTalk_20180520_163620948_hwMIF57.jpg"
                    }
                ]
            }
        }
    )
}
#수작업 배너
@permission_classes([AllowAny])
class BannerWeekly(APIView):
    @swagger_auto_schema(responses=response_schema_dict2)
    def get(self, request):
        """
            메인페이지 인기 배너

            # URL
                - GET /api/weekly/

        """
        hot_brand = Banner.objects.all().order_by('-view')
        results = hot_brand.values()
        result = []
        for each in results:
            each['brand_logo_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(Brand.objects.get(id=each['brand_id']).image)
            each['brand_banner_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(Brand.objects.get(id=each['brand_id']).banner_image)
            result.append(each)

        return JsonResponse({'result': result}, status=200)

@permission_classes([AllowAny])
# guest eventforyou, event
class PagenationTest1(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        category_id = data['category_id']
        brand_name = data['brand_name']
        try:
            page = request.GET['page']
        except:
            page = 1
        now = datetime.datetime.now()
        event = []
        result = []
        slice = 4  # 페이지마다 짜를 갯수
        default_slice = 10  # page=1 일때 디폴트 갯수
        size = (int(page) - 1) * slice
        next_page = 0
        if len(brand_name) == 0:
            events = Event.objects.filter(category=category_id, due__gt=now).order_by('-id')
            for each in events.values():
                each['event_img_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(each['image'])
                brand = Brand.objects.get(id=each['brand_id'])
                ev = Event.objects.get(id=each['id'])
                event.append(each)
                event[-1]['brand_name'] = brand.name
                event[-1]['d-day'] = (ev.due - now).days
            # 페이지네이션 next_page 설정
            if len(event) <= default_slice + size:
                next_page = -1
            else:
                next_page = int(page) + 1
            if int(page) == 1:
                for i in range(0, default_slice):
                    if len(event) <= i:
                        return JsonResponse({'event': result, 'next_page': next_page}, status=200)
                    result.append(event[i])
            else:
                for i in range(default_slice + (int(page) - 2) * slice, default_slice + size):
                    if len(event) <= i:
                        return JsonResponse({'event': result, 'next_page': next_page}, status=200)
                    result.append(event[i])

        else:
            for i in brand_name:
                br = Brand.objects.get(name=i)
                events = Event.objects.filter(brand=br.id, category=category_id, due__gt=now).order_by('-id')
                for each in events.values():
                    each['event_img_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(each['image'])
                    brand = Brand.objects.get(id=each['brand_id'])
                    ev = Event.objects.get(id=each['id'])
                    event.append(each)
                    event[-1]['brand_name'] = brand.name
                    event[-1]['d-day'] = (ev.due - now).days
            # 페이지네이션 next_page 설정
            if len(event) <= default_slice + size:
                next_page = -1
            else:
                next_page = int(page) + 1
            if int(page) == 1:
                for i in range(0, default_slice):
                    if len(event) <= i:
                        return JsonResponse({'event': result, 'next_page': next_page}, status=200)
                    result.append(event[i])
            else:
                for i in range(default_slice + (int(page) - 2) * slice, default_slice + size):
                    if len(event) <= i:
                        return JsonResponse({'event': result, 'next_page': next_page}, status=200)
                    result.append(event[i])

        return JsonResponse({'event': result, 'next_page': next_page}, status=200)

class PagenationTest2(APIView):
    # 회원 event
    def post(self, request):
        data = JSONParser().parse(request)
        category_id = data['category_id']
        brand_name = data['brand_name']
        user_id = request.user.id
        subscribes = SubscribeEvent.objects.filter(user=user_id)
        now = datetime.datetime.now()
        event = []
        try:
            page = request.GET['page']
        except:
            page = 1
        slice = 4   # 페이지마다 짜를 갯수
        default_slice = 10  # page=1 일때 디폴트 갯수
        size = (int(page) - 1) * slice
        result = []
        next_page = 0
        if len(brand_name) == 0:
            events = Event.objects.filter(category=category_id, due__gt=now).order_by('-id')
            for each_event in events.values():
                ev = Event.objects.get(id=each_event['id'])
                # 이벤트 사진 url
                each_event['event_img_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(each_event['image'])
                for each_sub in subscribes:
                    if each_sub.event.id == each_event['id']:
                        brand = Brand.objects.get(id=each_event['brand_id'])
                        event.append(each_event)
                        event[-1]['brand_name'] = brand.name
                        event[-1]['subs'] = True
                        event[-1]['d-day'] = (ev.due - now).days
                        break
                else:
                    brand = Brand.objects.get(id=each_event['brand_id'])
                    event.append(each_event)
                    event[-1]['brand_name'] = brand.name
                    event[-1]['subs'] = False
                    event[-1]['d-day'] = (ev.due - now).days
            # 페이지네이션 next_page 설정
            if len(event) <= default_slice + size:
                next_page = -1
            else:
                next_page = int(page) + 1
            if int(page) == 1:
                for i in range(0, default_slice):
                    if len(event) <= i:
                        return JsonResponse({'event': result, 'next_page': next_page}, status=200)
                    result.append(event[i])
            else:
                for i in range(default_slice + (int(page) - 2) * slice, default_slice + size):
                    if len(event) <= i:
                        return JsonResponse({'event': result, 'next_page': next_page}, status=200)
                    result.append(event[i])

        else:
            for i in brand_name:
                try:
                    br = Brand.objects.get(name=i)
                    events = Event.objects.filter(brand=br.id, category=category_id, due__gt=now).order_by('-id')
                    for each_event in events.values():
                        ev = Event.objects.get(id=each_event['id'])
                        each_event['event_img_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(each_event['image'])
                        for each_sub in subscribes:
                            if each_sub.event.id == each_event['id']:
                                brand = Brand.objects.get(id=each_event['brand_id'])
                                event.append(each_event)
                                event[-1]['brand_name'] = brand.name
                                event[-1]['subs'] = True
                                event[-1]['d-day'] = (ev.due - now).days
                                break
                        else:
                            brand = Brand.objects.get(id=each_event['brand_id'])
                            event.append(each_event)
                            event[-1]['brand_name'] = brand.name
                            event[-1]['subs'] = False
                            event[-1]['d-day'] = (ev.due - now).days
                except Exception as e:
                    continue
            # 페이지네이션 next_page 설정
            if len(event) <= size:
                next_page = -1
            else:
                next_page = int(page) + 1
            if int(page) == 1:
                for i in range(0, default_slice):
                    if len(event) <= i:
                        return JsonResponse({'event': result, 'next_page': next_page}, status=200)
                    result.append(event[i])
            else:
                for i in range((int(page) - 1) * slice, size):
                    if len(event) <= i:
                        return JsonResponse({'event': result, 'next_page': next_page}, status=200)
                    result.append(event[i])

        return JsonResponse({'event': result, 'next_page': next_page}, status=200)
