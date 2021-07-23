
# coding=utf-8
from rest_framework import status, mixins

# FBV
from rest_framework.response import Response

from rest_framework import generics  # generics class-based view 사용할 계획
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes
from django.contrib.auth.decorators import login_required

# JWT 사용을 위해 필요
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from .serializers import *
from .models import *
from .forms import *


# 회원가입
@permission_classes([AllowAny])
class Registration(generics.GenericAPIView):
    """
        회원가입
        ---
        # URL
            - POST /accounts/create/
        # 전달 형식 : formdata
            - { username : string,
                password1 : string, //비밀번호
                password2 : string, //확인용 다시치는 비밀번호
                nickname : string,
                email : string,
                gender : string,
                birth : date,
                }
     """
    serializer_class = CustomRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        serializer.is_valid(raise_exception=True)
        user = serializer.save(request)  # request 필요 -> 오류 발생
        return Response(
            {
                # get_serializer_context: serializer에 포함되어야 할 어떠한 정보의 context를 딕셔너리 형태로 리턴
                # 디폴트 정보 context는 request, view, format
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data
            },
            status=status.HTTP_201_CREATED,
        )


# 회원 정보 수정
class Update(generics.GenericAPIView):
    """
        회원 수정
        ---
        # URL
            - POST /accounts/update/
        #header
            - Authorization : JWT ey93... [jwt token]
        # 전달 형식 : formdata
            - {
                nickname : string,
                email : string,
                gender : string,
                birth : date,
                }
     """
    serializer_class = UpdateSerializer

    def post(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        user = request.user
        user.birth = request.POST["birth"]
        user.gender = request.POST["gender"]
        user.nickname = request.POST["nickname"]
        user.save()
        # if not form.is_valid():
        #     return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        return Response(
            {
                # get_serializer_context: serializer에 포함되어야 할 어떠한 정보의 context를 딕셔너리 형태로 리턴
                # 디폴트 정보 context는 request, view, format
                "name": user.username,
            },
            status=status.HTTP_201_CREATED,
        )


# 회원 탈퇴
@permission_classes([IsAuthenticated])
class Unsubscribe(generics.GenericAPIView):
    """
        회원 탈퇴
        ---
        # URL
            - POST /accounts/unsubscribe/
        # header
            - Authorization : JWT ey93... [jwt token]
        # 전달 형식 : formdata
            - {
                username : string   //본인확인용
               }
     """
    serializer_class = UnsubscribeSerializer

    def post(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        user = request.user
        if user.username == request.POST["username"]:
            user.delete()
            return Response(
                {
                    "success": True,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "success": False,
                    "user" : user.username,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )


#로그인
@permission_classes([AllowAny])
class Login(generics.GenericAPIView):
    """
        메인페이지의 EventForYou 이벤트 목록을 불러오는 API
        ---
        # 예시
            - POST /api/eventforyou/
        # parameter
            - {user : 1} : user 의 id 를 JSON형식으로 전달

     """
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if user['username'] == "None":
            return Response({"message": "fail"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": user['token']
            }
        )

