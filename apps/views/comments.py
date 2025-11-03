from django.db.models.aggregates import Count
from django.utils.timezone import now
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Answer, AnswerComment
from apps.models import Comment, Question
from apps.serializers import AnswerCommentModelSerializer
from apps.serializers import CommentModelSerializer
from apps.serializers import ContributorSerializer, CommunityStatsSerializer
from authentication.models import User


# ==================================================================Comment


@extend_schema(tags=['block-comment'])
class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentModelSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema(tags=['block-comment'])
class CommentListAPIView(ListAPIView):
    serializer_class = CommentModelSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        query = super().get_queryset()
        pk = self.kwargs.get('pk')
        query = query.filter(blog_id=pk).all()
        return query


@extend_schema(tags=['block-comment'])
class CommentDestroyAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['answer-comment'])
class AnswerCommentCreateAPIView(CreateAPIView):
    serializer_class = AnswerCommentModelSerializer
    queryset = AnswerComment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema(tags=['answer-comment'])
class AnswerCommentListAPIView(ListAPIView):
    serializer_class = AnswerCommentModelSerializer
    queryset = AnswerComment.objects.all()


@extend_schema(tags=['answer-comment'])
class AnswerCommentDeleteAPIView(DestroyAPIView):
    serializer_class = AnswerCommentModelSerializer
    queryset = AnswerComment.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['answer-comment'])
class AnswerCommentUpdateAPIView(UpdateAPIView):
    serializer_class = AnswerCommentModelSerializer
    queryset = AnswerComment.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['statistics'])
class CommunityStatsView(APIView):
    def get(self, request):
        total_questions = Question.objects.count()

        answered_today = Answer.objects.filter(created_at__date=now().date()).count()

        active_users = (
            User.objects
            .annotate(
                contributions=Count('questions', distinct=True) + Count('answers', distinct=True)
            )
            .filter(contributions__gte=3)
            .count()
        )

        top_contributors_qs = (
            User.objects
            .annotate(
                total_contributions=Count('questions', distinct=True) + Count('answers', distinct=True)
            )
            .order_by('-total_contributions')[:3]
        )
        contributors_data = ContributorSerializer(top_contributors_qs, many=True).data

        stats_data = {
            "total_questions": total_questions,
            "active_users": active_users,
            "answered_today": answered_today,
            "top_contributors": contributors_data,
        }

        serializer = CommunityStatsSerializer(stats_data)
        return Response(serializer.data)
