import random
from http import HTTPStatus

from django.contrib.auth.models import User
from django.core.cache import cache
from django.shortcuts import render
from django.utils.timezone import now
from drf_spectacular.utils import extend_schema
from google.auth.transport import requests
from google.oauth2 import id_token
from orjson import orjson
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.models import User, Sessions
from authentication.serializers import UserModelSerializer, SessionModelSerializer
from authentication.serializers import VerifyCodeSerializer
from authentication.tasks import send_code_email
from root.settings import GOOGLE_CLIENT_ID, MAIN_URL


@extend_schema(tags=['auth'])
class UserGenericAPIView(GenericAPIView):
    serializer_class = UserModelSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        code = str(random.randrange(10 ** 5, 10 ** 6))
        send_code_email(user, code)

        # Redis o‘rniga cache
        cache.set(code, orjson.dumps(user), timeout=300)  # 5 daqiqaga saqlanadi

        return Response({'message': 'Tasdiqlash kodi jo‘natildi'}, status=HTTPStatus.OK)


@extend_schema(tags=['auth'])
class VerifyCodeGenericAPIView(GenericAPIView):
    serializer_class = VerifyCodeSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.context.get('user_data')
        user = User.objects.create(**user_data)
        return Response(UserModelSerializer(user).data, status=HTTPStatus.CREATED)


@extend_schema(tags=['auth'])
class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        original_response = super().post(request, *args, **kwargs)
        if original_response.status_code == 200 and 'access' in original_response.data:
            email = request.data.get('email')
            user = User.objects.filter(email=email).first()
            device = {
                'device_name': request.META.get('HTTP_USER_AGENT', 'Unknown'),
                'ip_address': request.META.get('REMOTE_ADDR', '127.0.0.1'),
            }
            query = Sessions.objects.filter(device_name=device['device_name'])
            sessions = Sessions.objects.filter(user=user)
            if not query.exists():
                if sessions.count() >= 3:
                    serializer = SessionModelSerializer(instance=sessions, many=True)
                    return Response(data=serializer.data, status=HTTPStatus.OK)
                else:
                    Sessions.objects.create(user=user, **device)
            user.last_login = now()
            user.save(update_fields=["last_login"])
        return original_response


@extend_schema(tags=['auth'])
class CustomTokenRefreshView(TokenRefreshView):
    pass


def auth_google(request):
    return render(request, 'auth.html', context={'client_id': GOOGLE_CLIENT_ID, 'main_url': MAIN_URL})


@extend_schema(tags=['auth'])
class GoogleAuthView(APIView):
    def post(self, request):
        token = request.data.get("token")
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            email = idinfo.get("email")
            name = idinfo.get("name")
            user, created = User.objects.get_or_create(
                email=email,
                defaults={"username": name}
            )
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)

        except ValueError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
