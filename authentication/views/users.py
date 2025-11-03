from http import HTTPStatus

from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, GenericAPIView
from rest_framework.response import Response

from authentication.models import User
from authentication.serializers import UserModelSerializer, UserUpdateSerializer, ChangePasswordSerializer


@extend_schema(tags=['user'])
class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'pk'


@extend_schema(tags=['user'])
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    filter_backends = [SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']


@extend_schema(tags=['user'])
class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = 'pk'


@extend_schema(tags=['user'])
class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


@extend_schema(tags=['user'])
class ChangePasswordAPIView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Parol muvaffaqiyatli o‘zgartirildi"},
            status=HTTPStatus.OK
        )
