from http import HTTPStatus

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response

from authentication.models import Follow, Notifications
from authentication.serializers import FollowingModelSerializer, NotificationModelSerializer


@extend_schema(tags=['follow'])
class FollowingCreateAPIView(CreateAPIView):
    serializer_class = FollowingModelSerializer

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


@extend_schema(tags=['follow'], parameters=[
    OpenApiParameter(
        name='type',
        description='enter follower',
        required=False,
        type=str
    )
])
class FollowsListAPiView(ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowingModelSerializer

    def get_queryset(self):
        query = super().get_queryset()
        type = self.request.query_params.get('type')
        if type == 'followed':
            query = query.filter(follower=self.request.user)
        if type == 'following':
            query = query.filter(following=self.request.user)
        return query


@extend_schema(tags=['follow'])
class FollowDestroyAPIView(DestroyAPIView):
    queryset = Follow.objects.all()
    lookup_field = 'pk'

    def get_object(self):
        follow_id = self.kwargs.get(self.lookup_field)
        obj = Follow.objects.filter(following=follow_id).first()
        if not obj:
            raise NotFound("Follow topilmadi yoki sizga tegishli emas")
        return obj

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return Response({'message': 'Muvofaqiyatli ochirildi'}, status=HTTPStatus.NO_CONTENT)


# ======================================================notifications================================


@extend_schema(tags=['notifications'], parameters=[
    OpenApiParameter(
        name='type',
        required=False,
        type=Notifications.NotificationType,
    )
])
class NotificationsListAPIView(ListAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationModelSerializer

    def get_queryset(self):
        query = super().get_queryset()

        type = self.request.query_params.get('type')
        if type == 'followed':
            query = query.filter(type=Notifications.NotificationType.FOLLOWED)
        if type == 'liked':
            query = query.filter(type=Notifications.NotificationType.LIKED)
        if type == 'commented':
            query = query.filter(type=Notifications.NotificationType.COMMENTED)
        if type == 'saved':
            query = query.filter(type=Notifications.NotificationType.SAVED)
        return query.filter(recipient=self.request.user)
