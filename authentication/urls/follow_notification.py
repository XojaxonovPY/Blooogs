from django.urls import path

from authentication.views import *

urlpatterns = [
    path('following/', FollowingCreateAPIView.as_view()),
    path('follows/list/', FollowsListAPiView.as_view()),
    path('following/delete/<int:pk>', FollowDestroyAPIView.as_view()),
    path('notifications', NotificationsListAPIView.as_view()),
]
