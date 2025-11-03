from http import HTTPStatus

from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.models import Blog, BlogImages, Save
from apps.models import BlogView
from apps.serializers import BlogModelSerializer, BlogImagesModelSerializer, LikeSerializer, SaveModelSerializer
from authentication.models import Notifications


@extend_schema(tags=['blog'])
class BlogCreateAPIView(CreateAPIView):
    serializer_class = BlogModelSerializer
    queryset = Blog.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema(tags=['blog'])
class BlogListAPIView(ListAPIView):
    serializer_class = BlogModelSerializer
    queryset = Blog.objects.all()


@extend_schema(tags=['blog'])
class BlogDestroyAPIView(DestroyAPIView):
    serializer_class = BlogModelSerializer
    queryset = Blog.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['blog'])
class BlogUpdateAPIView(UpdateAPIView):
    serializer_class = BlogModelSerializer
    queryset = Blog.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['blog'])
class BlogDetailAPIView(RetrieveAPIView):
    serializer_class = BlogModelSerializer
    queryset = Blog.objects.all()
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_authenticated:
            BlogView.objects.get_or_create(blog=instance, user=request.user)

        serializer = self.get_serializer(instance)
        data = serializer.data
        data['views'] = instance.blog_views.count()
        return Response(data)


@extend_schema(tags=['blog-images'])
class BlogImagesCreateAPIView(CreateAPIView):
    serializer_class = BlogImagesModelSerializer
    queryset = BlogImages.objects.all()


@extend_schema(tags=['blog-images'])
class BlogImagesUpdateAPIView(UpdateAPIView):
    serializer_class = BlogImagesModelSerializer
    queryset = BlogImages.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['blog-images'])
class BlogImagesDetailAPIView(RetrieveAPIView):
    serializer_class = BlogImagesModelSerializer
    queryset = BlogImages.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['blog-images'])
class BlogImagesDestroyAPIView(DestroyAPIView):
    serializer_class = BlogImagesModelSerializer
    queryset = BlogImages.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['blog-images'])
class BlogImagesListAPIView(ListAPIView):
    serializer_class = BlogImagesModelSerializer
    queryset = BlogImages.objects.all()


# ==================================================================Like

@extend_schema(tags=['blog-like'])
class LikeGenericAPIView(GenericAPIView):
    serializer_class = LikeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        blog = serializer.blog_data
        blog.likes.add(request.user)
        if blog.author != request.user:
            Notifications.objects.create(
                recipient=blog.author,
                sender=request.user,
                message='liked your post',
                type=Notifications.NotificationType.LIKED.value
            )
        return Response({'message': 'like bosildi'}, status=HTTPStatus.OK)


@extend_schema(tags=['blog-like'])
class LikeCountAPIView(GenericAPIView):
    def get(self, request, pk):
        blog = Blog.objects.filter(pk=pk).first()
        quantity = blog.likes.count()
        return Response({'count': quantity}, status=HTTPStatus.OK)


@extend_schema(tags=['blog-like'])
class LikeRemoveAPIView(GenericAPIView):
    serializer_class = LikeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        blog = serializer.blog_data
        blog.likes.remove(request.user)
        return Response({'message': 'like olibtashlandi'}, status=HTTPStatus.NO_CONTENT)


# ==================================================================Save=========================================

@extend_schema(tags=['save'])
class SaveModelViewSet(ModelViewSet):
    queryset = Save.objects.all()
    serializer_class = SaveModelSerializer
    http_method_names = ['post', 'get', 'delete']
    lookup_field = 'pk'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        query = super().get_queryset()
        return query.filter(user=self.request.user)
