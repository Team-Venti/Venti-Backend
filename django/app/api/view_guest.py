# coding=utf-8
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
import datetime
from .models import Event, Brand
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import datetime

@permission_classes([AllowAny])
class BrandList(APIView):
    '''
    비회원일때 api
    GET api/guest/brand_list/ - 회원가입시 선호브랜드
    - request
    {
        x
    }
    '''
    response_schema_dict2 = {
        "200": openapi.Response(
            description="회원가입 시 선호브랜드에서 브랜드 목록 불러옴",
            examples={
                "application/json": {
                    "brand": [
                        {
                            "id": 1,
                            "created_date": "2021-08-04",
                            "update_date": "2021-08-04",
                            "category_id": 1,
                            "image": "brand_logo/무신사배너.jpeg",
                            "banner_image": "brand_banner/무신사페이.jpeg",
                            "name": "aa",
                            "text": "ddd",
                            "brand_logo_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_logo/무신사배너.jpeg",
                            "brand_banner_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_banner/무신사페이.jpeg"
                        },
                        {
                            "id": 2,
                            "created_date": "2021-08-04",
                            "update_date": "2021-08-04",
                            "category_id": 1,
                            "image": "brand_logo/버거킹.png",
                            "banner_image": "brand_banner/버거킹배너.jpeg",
                            "name": "bb",
                            "text": "bbb",
                            "brand_logo_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_logo/버거킹.png",
                            "brand_banner_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_banner/버거킹배너.jpeg"
                        }
                    ]
                }
            }
        )
    }
    @swagger_auto_schema(responses=response_schema_dict2)
    def get(self, request):
        """
            회원가입 선호브랜드 할때 브랜드 목록 불러옴

            # URL
                - GET /api/guest/brand_list/

        """
        brands = Brand.objects.filter(category=1).order_by('name')
        brand2 = Brand.objects.filter(category=2).order_by('name')
        brand3 = Brand.objects.filter(category=3).order_by('name')
        brands = brands.union(brand2)
        brands = brands.union(brand3)
        brand = brands.values()
        brand_list = []
        for i in brand:
            i['brand_logo_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(i['image'])
            i['brand_banner_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(i['banner_image'])
            brand_list.append(i)

        return JsonResponse({'brand': brand_list}, status=200)


@permission_classes([AllowAny])
class BrandMain(APIView):
    '''
    비회원일때 api
    POST api/guest/brand_main/ - 브랜드 메인
    - request
    {
        "category_id" : int (category id)
    }
    '''
    response_schema_dict3 = {
        "200": openapi.Response(
            description="카테고리 별 브랜드 목록",
            examples={
                "application/json": {
                    "brand": [
                        {
                            "id": 1,
                            "created_date": "2021-08-04",
                            "update_date": "2021-08-04",
                            "category_id": 1,
                            "image": "brand_logo/무신사배너.jpeg",
                            "banner_image": "brand_banner/무신사페이.jpeg",
                            "name": "aa",
                            "text": "ddd",
                            "brand_logo_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_logo/무신사배너.jpeg",
                            "brand_banner_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_banner/무신사페이.jpeg"
                        },
                        {
                            "id": 2,
                            "created_date": "2021-08-04",
                            "update_date": "2021-08-04",
                            "category_id": 1,
                            "image": "brand_logo/버거킹.png",
                            "banner_image": "brand_banner/버거킹배너.jpeg",
                            "name": "bb",
                            "text": "bbb",
                            "brand_logo_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_logo/버거킹.png",
                            "brand_banner_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_banner/버거킹배너.jpeg"
                        }
                    ]
                }
            }
        )
    }
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'category_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='int'),
        }
    ), responses=response_schema_dict3)
    def post(self, request, format=None):
        """
            (비회원일때) 카테고리 별 브랜드 목록

            # URL
                - POST /api/guest/brand_main/

        """
        data = JSONParser().parse(request)
        category_id = data['category_id']
        brands = Brand.objects.filter(category=category_id).order_by('name')
        brand = brands.values()
        brand_list = []
        for i in brand:
            i['brand_logo_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(i['image'])
            i['brand_banner_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(i['banner_image'])
            brand_list.append(i)
        return JsonResponse({'brand': brand_list}, status=200)


@permission_classes([AllowAny])
class BrandDetail(APIView):
    '''
    비회원일때 api
    POST api/guest/brand_detail/ - 브랜드 상세
    - request
    {
        "brand_id" : int (brand id)
    }
    '''
    response_schema_dict1 = {
        "200": openapi.Response(
            description="브랜드 상세",
            examples={
                "application/json": {
                    "brand": [
                        {
                            "id": 1,
                            "created_date": "2021-08-04",
                            "update_date": "2021-08-04",
                            "category_id": 1,
                            "image": "brand_logo/무신사배너.jpeg",
                            "banner_image": "brand_banner/무신사페이.jpeg",
                            "name": "aa",
                            "text": "ddd",
                            "brand_logo_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_logo/무신사배너.jpeg",
                            "brand_banner_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/brand_banner/무신사페이.jpeg"
                        }
                    ]
                }
            }
        )
    }
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'brand_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='int')
        }
    ), responses=response_schema_dict1)
    def post(self, request, format=None):
        """
            (비회원일때) 브랜드 상세

            # URL
                - POST /api/guest/brand_detail/

        """
        data = JSONParser().parse(request)
        brand_id = data['brand_id']
        brands = Brand.objects.filter(id=brand_id)
        # brand = brands.values()
        # brand_list = []
        brand = brands.values()[0]
        brand['brand_logo_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(brand['image'])
        brand['brand_banner_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(brand['banner_image'])

        return JsonResponse({'brand': brand}, status=200)


@permission_classes([AllowAny])
class EventMain(APIView):
    '''
    비회원일때 api
    POST api/guest/event_main/ - 이벤트 메인, 비회원일때 eventforyou
    - request
    {
        "category_id" : int (category id),
        "brand_id" : int array (brand id)
    }
    '''
    response_schema_dict4 = {
        "200": openapi.Response(
            description="카테고리, 브랜드 별 이벤트 목록을 불러옴",
            examples={
                "application/json": {
                     {
                "event": [
                    {
                        "id": 175,
                        "created_date": "2021-08-10T22:42:05.705",
                        "update_date": "2021-08-10T22:42:05.705",
                        "category_id": 1,
                        "brand_id": 15,
                        "name": "기라델리 민트초코 1+1",
                        "image": "event_logo/던킨도너츠_-_기라델리_민트초코_11.jpeg",
                        "text": "-",
                        "due": "2021-08-16T00:00:00",
                        "view": 2,
                        "url": "http://www.dunkindonuts.co.kr/event/view.php?S=4281&flag=",
                        "event_img_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/event_logo/던킨도너츠_-_기라델리_민트초코_11.jpeg",
                        "brand_name": "던킨도너츠",
                        "d-day": 4
                    },
                    {
                        "id": 174,
                        "created_date": "2021-08-10T22:41:27.458",
                        "update_date": "2021-08-10T22:41:27.458",
                        "category_id": 1,
                        "brand_id": 15,
                        "name": "DUNKIN X 카카오선물하기",
                        "image": "event_logo/던킨도너츠_-_카카오_선물하기_온라인_프로모션.jpeg",
                        "text": "-",
                        "due": "2021-08-16T00:00:00",
                        "view": 0,
                        "url": "http://www.dunkindonuts.co.kr/event/view.php?S=4273&flag=",
                        "event_img_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/event_logo/던킨도너츠_-_카카오_선물하기_온라인_프로모션.jpeg",
                        "brand_name": "던킨도너츠",
                        "d-day": 4
                    },
                    {
                        "id": 166,
                        "created_date": "2021-08-10T21:48:58.374",
                        "update_date": "2021-08-10T21:48:58.374",
                        "category_id": 1,
                        "brand_id": 2,
                        "name": "프리미엄와퍼 3900원",
                        "image": "event_logo/버거킹_이벤트_이미지_4.png",
                        "text": "1. 행사명 : 프리미엄와퍼 3900원\r\n\r\n2. 제품 : 통새우와퍼, 콰트로치즈와퍼, 할라피뇨와퍼\r\n\r\n3. 행사 기간 : 21년 8월 9일(월) ~ 8월 16일(월), 8일간\r\n\r\n4. 행사 시간 : 매장 운영시간에 따라 상이 합니다.\r\n\r\n5. 유의 사항 : \r\n\r\n*1인 5개까지만 판매\r\n\r\n*다른 할인 및 쿠폰과 중복 혜택 불가\r\n\r\n*딜리버리 주문 불가 및 예약 주문 불가\r\n\r\n*일부 매장은 행사에서 제외될 수 있습니다.\r\n\r\n*단체주문에서는 제외됩니다.\r\n\r\n*본 제품은 실제 이미지와 다를 수 있습니다.\r\n\r\n6. 제외매장\r\n대명비발디점, 삼성라이온즈파크점, 서울역점, 오션월드점, 인천공항1점, 인천공항교통센터1점, 경기양평점, 경남대점, 경남사천점, 경남삼천포점, 경북도청점, 경북상주점, 경북영주가흥점, 경주보문점, 광양LF스퀘어점, 광양중동점, 광주경안점, 광주매곡점, 광주봉선점, 광주상무점, 광주수완점, 광주월계점, 광주일곡점, 광주터미널점, 구미인의점, 군산나운FS점, 김천교동DT점, 김포현대아울렛점, 나주빛가람점, 당진읍내점, 대구대명FS점, 대구대점, 대구지산점, 대구칠곡3지구점, 대구테크노폴리스점, 대전관평점, 대전시청점, 대전현대아울렛점, 목포하당점, 보령동대점, 부산오시리아점, 서산호수공원점, 세종행복새롬점, 수원정자점, 순천법원점, 안동옥동점, 안동중앙점, 여수웅천점, 연희점, 오산궐동점, 오창호수공원점, 원광대점, 원주무실점, 의정부HP점, 익산영등점, 인천송도센트럴파크점, 인천연수점, 전남도청점, 정읍중앙점, 진주경상대점, 진주혁신도시점, 청주복대점, 청주율량점, 충남대병원DT점, 충남도청점, 충북진천점, 충주연수점, 평택비전점, 평택청북점, 한동대점, 해운대비치점, 호남대점",
                        "due": "2021-08-17T00:00:00",
                        "view": 4,
                        "url": "https://www.burgerking.co.kr/#/eventDetail/504",
                        "event_img_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/event_logo/버거킹_이벤트_이미지_4.png",
                        "brand_name": "버거킹",
                        "d-day": 5
                    },
                    {
                        "id": 165,
                        "created_date": "2021-08-10T21:43:43.895",
                        "update_date": "2021-08-10T21:43:43.895",
                        "category_id": 1,
                        "brand_id": 2,
                        "name": "제로톡톡 2종 각 1,500원",
                        "image": "event_logo/버거킹_이벤트_이미지_3.png",
                        "text": "1. 행사명 : 제로톡톡 2종 각 1,500원\r\n\r\n2. 행사기간 : 21년 8월 1일 ~ 21년 8월 31일  \r\n\r\n3. 행사제품 : 제로톡톡 청포도, 제로톡톡 복숭아 2종\r\n\r\n4. 내용 : 제로톡톡 2000원 -> 1500원 할인\r\n\r\n5. 유의사항\r\n\r\n*1인 5개까지만 판매\r\n\r\n*다른 할인 및 쿠폰과 중복 혜택 불가\r\n\r\n*딜리버리 주문 불가 및 예약 주문 불가\r\n\r\n*일부 매장은 행사에서 제외될 수 있습니다.\r\n\r\n*단체주문에서는 제외됩니다.\r\n\r\n*본 제품은 실제 이미지와 다를 수 있습니다.\r\n\r\n6. 제외매장 : \r\n경기양평점, 경남대점, 경남사천점, 경북도청점, 경북상주점, 경북영주가흥점, 경주보문점, 광양LF스퀘어점, 광양중동점, 광주상무점, 광주월계점, 광주일곡점, 광주터미널점, 구미산동점, 구미인의점, 군산나운FS점, 김천교동DT점, 김포현대아울렛점, 당진읍내점, 대구대명FS점, 대구대점, 대구죽전네거리점, 대구칠곡3지구점, 대구테크노폴리스점, 대명비발디점, 대전관평점, 대전도안점, 대전시청점, 대전현대아울렛점, 목포하당점, 방배카페골목점, 보령동대점, 부산안락DT점, 부산오시리아점, 삼성라이온즈파크점, 서울역점, 세종행복새롬점, 숭례문점, 안동옥동점, 여수웅천점, 연희점, 오션월드점, 인천공항1점, 인천공항교통센터1점, 인천송도센트럴파크점, 인천연수HP점, 인천연수점, 전남도청점, 전주중앙점, 천안두정점, 청주오송점, 충남대병원DT점, 충북대점, 충주연수점, 평택비전점, 평택청북점, 해운대우동점",
                        "due": "2021-09-01T00:00:00",
                        "view": 2,
                        "url": "https://www.burgerking.co.kr/#/eventDetail/503",
                        "event_img_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/event_logo/버거킹_이벤트_이미지_3.png",
                        "brand_name": "버거킹",
                        "d-day": 20
                    }
                ],
                "next_page": 3
                }
                }
            }
        )
    }
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'category_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='int'),
            'brand_name': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING),
                                       description='string')
        }
    ), responses=response_schema_dict4)
    def post(self, request, format=None):
        """
            (비회원일때) 카테고리, 브랜드 별 이벤트 목록 and (비회원일때) 메인페이지의 eventforyou

            # URL
                - POST /api/guest/event_main/
                - POST /api/guest/event_main/?page=1

        """
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


@permission_classes([AllowAny])
class EventDetail(APIView):
    '''
    비회원일때 api
    POST api/guest/event_detail/ - 이벤트 상세
    - request
    {
        "event_id" : int (event id)
    }
    '''
    response_schema_dict5 = {
        "200": openapi.Response(
            description="이벤트 상세",
            examples={
                "application/json": {
                    "event": [
                        {
                            "id": 1,
                            "created_date": "2021-08-04",
                            "update_date": "2021-08-04",
                            "category_id": 1,
                            "brand_id": 1,
                            "name": "aalike",
                            "image": "event_logo/버거킹배너.jpeg",
                            "text": "dd",
                            "due": "2021-08-07",
                            "view": 1,
                            "url": "https://magazine.musinsa.com/index.php?m=news&cat=EVENT&uid=47461",
                            "event_img_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/event_logo/버거킹배너.jpeg",
                            "brand_name": "aa"
                        }
                    ]
                }
            }
        )
    }
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'event_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='int')
        }
    ), responses=response_schema_dict5)
    def post(self, request, format=None):
        """
            (비회원일때) 이벤트 상세

            # URL
                - POST /api/guest/event_detail/

        """
        data = JSONParser().parse(request)
        event_id = data['event_id']
        events = Event.objects.filter(id=event_id)
        events.update(view=events[0].view+1)
        event = []
        now = datetime.datetime.now()
        for each_event in events.values():
            each_event['event_img_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(each_event['image'])
            brand = Brand.objects.get(id=each_event['brand_id'])
            ev = Event.objects.get(id=each_event['id'])
            event.append(each_event)
            event[-1]['brand_name'] = brand.name
            event[-1]['due'] = ev.due.strftime("%Y-%m-%d")

        return JsonResponse({'event': event}, status=200)


@permission_classes([AllowAny])
class EventDeadline(APIView):
    '''
    비회원일때 api
    POST api/guest/event_deadline/ - 브랜드 상세 눌렀을때 밑에 이벤트들
    - request
    {
        "brand_id" : int (brand id)
    }
    '''
    response_schema_dict6 = {
        "200": openapi.Response(
            description="브랜드 상세에서 해당 브랜드의 이벤트 목록을 불러옴",
            examples={
                "application/json": {
                    "on_event": [
                        {
                            "id": 1,
                            "created_date": "2021-08-04",
                            "update_date": "2021-08-04",
                            "category_id": 1,
                            "brand_id": 1,
                            "name": "aalike",
                            "image": "event_logo/버거킹배너.jpeg",
                            "text": "dd",
                            "due": "2021-08-07T10:27:49",
                            "view": 1,
                            "url": "https://magazine.musinsa.com/index.php?m=news&cat=EVENT&uid=47461",
                            "event_img_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/event_logo/버거킹배너.jpeg",
                            "brand_name": "aa",
                            "d-day": 1
                        },
                        {
                            "id": 2,
                            "created_date": "2021-08-04",
                            "update_date": "2021-08-04",
                            "category_id": 1,
                            "brand_id": 1,
                            "name": "aaunlike",
                            "image": "event_logo/버거킹.png",
                            "text": "dd",
                            "due": "2021-08-07T10:28:05",
                            "view": 1,
                            "url": "http://event.com",
                            "event_img_url": "https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/event_logo/버거킹.png",
                            "brand_name": "aa",
                            "d-day": 1
                        }
                    ],
                    "off_event": []
                }
            }
        )
    }
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'brand_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='int')
        }
    ), responses=response_schema_dict6)
    def post(self, request, format=None):
        """
            (비회원일때) 브랜드 상세에서 해당 브랜드의 이벤트 목록

            # URL
                - POST /api/guest/event_deadline/

        """
        data = JSONParser().parse(request)
        brand_id = data['brand_id']
        on_event = []
        off_event = []
        now = datetime.datetime.now()
        events = Event.objects.filter(brand=brand_id)
        for each_event in events.values():
            each_event['event_img_url'] = 'https://venti-s3.s3.ap-northeast-2.amazonaws.com/media/' + str(each_event['image'])
            brand = Brand.objects.get(id=each_event['brand_id'])
            ev = Event.objects.get(id=each_event['id'])
            if each_event['due'] > now:
                on_event.append(each_event)
                on_event[-1]['brand_name'] = brand.name
                on_event[-1]['d-day'] = (ev.due - now).days
            else:
                off_event.append(each_event)
                off_event[-1]['brand_name'] = brand.name
                off_event[-1]['d-day'] = (ev.due - now).days

        return JsonResponse({"on_event": on_event,
                             "off_event": off_event}, status=200)
