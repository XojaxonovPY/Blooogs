from http import HTTPStatus

from django.db.models.aggregates import Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response

from apps.models import Question
from apps.models import QuestionView
from apps.serializers import QuestionModelSerializer
from apps.serializers import QuestionVotesSerializer


@extend_schema(tags=['question'])
class QuestionCreateAPIView(CreateAPIView):
    serializer_class = QuestionModelSerializer
    queryset = Question.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema(
    tags=['question'],
    parameters=[
        OpenApiParameter(
            name='filter',
            description="Filter questions: 'recent', 'popular', 'unanswered'",
            required=False,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name='search',
            description="Search by title or content",
            required=False,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
        ),
    ],
)
class QuestionListAPIView(ListAPIView):
    serializer_class = QuestionModelSerializer
    queryset = Question.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content']

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_type = self.request.query_params.get('filter')

        if filter_type == 'recent':
            queryset = queryset.order_by('-created_at')

        elif filter_type == 'popular':
            queryset = queryset.annotate(
                views_count=Count('question_views')
            ).order_by('-views_count')

        elif filter_type == 'unanswered':
            queryset = queryset.annotate(
                answers_count=Count('answers')
            ).filter(answers_count=0).order_by('-created_at')

        return queryset


@extend_schema(tags=['question'])
class QuestionDeleteAPIView(DestroyAPIView):
    serializer_class = QuestionModelSerializer
    queryset = Question.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['question'])
class QuestionUpdateAPIView(UpdateAPIView):
    serializer_class = QuestionModelSerializer
    queryset = Question.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['question'])
class QuestionDetailAPIView(RetrieveAPIView):
    serializer_class = QuestionModelSerializer
    queryset = Question.objects.all()
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_authenticated:
            QuestionView.objects.get_or_create(question=instance, user=request.user)

        serializer = self.get_serializer(instance)
        data = serializer.data
        data['views'] = instance.question_views.count()
        return Response(data)


# ==================================================================Votes

@extend_schema(tags=['question-vote'])
class QuestionVoteGenericAPIView(GenericAPIView):
    serializer_class = QuestionVotesSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.question_data
        question.votes.add(request.user)
        return Response({'message': 'vote bosildi'}, status=HTTPStatus.OK)


@extend_schema(tags=['question-vote'])
class QuestionVoteCountAPIView(GenericAPIView):
    def get(self, request, pk):
        question = Question.objects.filter(pk=pk).first()
        count = question.votes.count()
        return Response({'count': count}, status=HTTPStatus.OK)


@extend_schema(tags=['question-vote'])
class QuestionVoteRemoveAPIView(GenericAPIView):
    serializer_class = QuestionVotesSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.question_data
        question.votes.remove(request.user)
        return Response({'message': 'vote olindi'}, status=HTTPStatus.OK)

# ==================================================================Upvotes-Downvotes================================
