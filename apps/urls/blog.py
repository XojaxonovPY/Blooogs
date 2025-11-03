from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import *

router = DefaultRouter()
router.register(r'saves', SaveModelViewSet, basename='saves')

urlpatterns = [
    path('blog-create', BlogCreateAPIView.as_view()),
    path('blogs', BlogListAPIView.as_view()),
    path('blog-delete/<int:pk>', BlogDestroyAPIView.as_view()),
    path('blog-update/<int:pk>', BlogUpdateAPIView.as_view()),
    path('blog-detail/<int:pk>', BlogDetailAPIView.as_view()),
]

# blog-images
urlpatterns += [
    path('blog-images-create', BlogImagesCreateAPIView.as_view()),
    path('blogs', BlogImagesListAPIView.as_view()),
    path('blog-images-detail/<int:pk>', BlogImagesDetailAPIView.as_view()),
    path('blog-images-update/<int:pk>', BlogImagesUpdateAPIView.as_view()),
    path('blog-images-delete/<int:pk>', BlogImagesDestroyAPIView.as_view()),
]

urlpatterns += [
    path('blog/like', LikeGenericAPIView.as_view()),
    path('blog/like/count/<int:pk>', LikeCountAPIView.as_view()),
    path('blog/like/remove', LikeRemoveAPIView.as_view()),
]

urlpatterns += [
    path('save/', include(router.urls))
]
