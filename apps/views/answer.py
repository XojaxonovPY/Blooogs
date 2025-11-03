from http import HTTPStatus

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response

from apps.models import Answer, AnswerView
from apps.serializers import AnswerModelSerializer
from apps.serializers import AnswerVotesSerializer


@extend_schema(tags=['answers'])
class AnswerCreateAPIView(CreateAPIView):
    serializer_class = AnswerModelSerializer
    queryset = Answer.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema(tags=['answers'])
class AnswerListAPIView(ListAPIView):
    serializer_class = AnswerModelSerializer
    queryset = Answer.objects.all()


@extend_schema(tags=['answers'])
class AnswerDeleteAPIView(DestroyAPIView):
    serializer_class = AnswerModelSerializer
    queryset = Answer.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['answers'])
class AnswerUpdateAPIView(UpdateAPIView):
    serializer_class = AnswerModelSerializer
    queryset = Answer.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['answers'])
class AnswerDetailAPIView(RetrieveAPIView):
    serializer_class = AnswerModelSerializer
    queryset = Answer.objects.all()
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_authenticated:
            AnswerView.objects.get_or_create(answer=instance, user=request.user)

        serializer = self.get_serializer(instance)
        data = serializer.data
        data['views'] = instance.answer_views.count()
        return Response(data)


@extend_schema(tags=['answer-vote'], parameters=[
    OpenApiParameter(
        type=str,
        name='votes',
        required=False
    )
])
class AnswerVoteGenericAPIView(GenericAPIView):
    serializer_class = AnswerVotesSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answer = serializer.answer_data
        votes = request.query_params.get('votes')
        type = None
        if votes == 'upvote':
            answer.upvotes.add(request.user)
            type = 'upvote'
        if votes == 'downvote':
            answer.downvotes.add(request.user)
            type = 'downvote'
        return Response({'message': f'{type} bosildi'}, status=HTTPStatus.OK)


@extend_schema(tags=['question-vote'], parameters=[
    OpenApiParameter(
        type=str,
        name='votes',
        required=False
    ),
])
class AnswerVoteCountAPIView(GenericAPIView):

    def get(self, request, pk):
        answer = Answer.objects.filter(pk=pk).first()
        votes = request.query_params.get('votes')
        type = None
        count = 0
        if votes == 'upvote':
            count = answer.upvotes.count()
            type = 'upvote'
        if votes == 'downvote':
            count = answer.downvotes.count()
            type = 'downvote'
        return Response({'message': f'{type} soni{count}'}, status=HTTPStatus.OK)


@extend_schema(tags=['answer-vote'], parameters=[
    OpenApiParameter(
        type=str,
        name='votes',
        required=False
    ),
])
@extend_schema(tags=['answer-vote'])
class AnswerVoteRemoveAPIView(GenericAPIView):
    serializer_class = AnswerVotesSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answer = serializer.answer_data
        votes = request.query_params.get('votes')
        type = None
        if votes == 'upvote':
            answer.upvotes.remove(request.user)
            type = 'upvote'
        if votes == 'downvote':
            answer.downvotes.remove(request.user)
            type = 'downvote'
        return Response({'message': f'{type} olindi'}, status=HTTPStatus.OK)
