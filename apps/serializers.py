from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import Blog, BlogImages, Comment, AnswerComment, BlogView, AnswerView, QuestionView, Save
from apps.models import Question, Answer
from authentication.models import User, Notifications
from authentication.serializers import UserModelSerializer


class BlogModelSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'tags')
        read_only_fields = ('id', 'created_at', 'author')


class BlogViewModelSerializer(ModelSerializer):
    class Meta:
        model = BlogView
        fields = ('user',)
        read_only_fields = ('viewed_at',)


class LikeSerializer(Serializer):
    blog = IntegerField(required=True)

    def validate_blog(self, value):
        blog = Blog.objects.filter(pk=value).first()
        self.blog_data = blog
        return blog


class QuestionVotesSerializer(Serializer):
    question = IntegerField(required=True)

    def validate_question(self, value):
        question = Question.objects.filter(pk=value).first()
        self.question_data = question
        return value


class AnswerVotesSerializer(Serializer):
    answer = IntegerField(required=True)

    def validate_answer(self, value):
        answer = Answer.objects.filter(pk=value).first()
        self.answer_data = answer
        return value


class BlogImagesModelSerializer(ModelSerializer):
    class Meta:
        model = BlogImages
        fields = ('id', 'blog', 'image')
        read_only_fields = ('id',)


class QuestionModelSerializer(ModelSerializer):
    total_answers = SerializerMethodField()
    author = UserModelSerializer(many=False, read_only=True)

    class Meta:
        model = Question
        fields = ('title', 'content', 'author', 'is_edited', 'total_answers')
        read_only_fields = ('created_at', 'author', 'is_edited')

    def update(self, instance, validated_data):
        old_content = instance.content
        new_content = validated_data.get('content', old_content)

        if new_content != old_content:
            validated_data['is_edited'] = True

        return super().update(instance, validated_data)

    def get_total_answers(self, obj):
        return obj.answers.count()


class QuestionViewModelSerializer(ModelSerializer):
    class Meta:
        model = QuestionView
        fields = ('user',)
        read_only_fields = ('viewed_at',)


class AnswerModelSerializer(ModelSerializer):
    author = UserModelSerializer(many=False, read_only=True)

    class Meta:
        model = Answer
        fields = ('content', 'author', 'question', 'is_edited')
        read_only_fields = ('created_at', 'author', 'is_edited',)

    def update(self, instance, validated_data):
        old_content = instance.content
        new_content = validated_data.get('content', old_content)

        if new_content != old_content:
            validated_data['is_edited'] = True

        return super().update(instance, validated_data)


class AnswerViewModelSerializer(ModelSerializer):
    class Meta:
        model = AnswerView
        fields = ('user',)
        read_only_fields = ('viewed_at',)


class CommentModelSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'created_at', 'blog')
        read_only_fields = ('id', 'created_at', 'author')

    def validate_blog(self, value):
        recipient = value.author
        sender = self.context["request"].user
        if sender != recipient:
            Notifications.objects.create(
                recipient=recipient,
                sender=sender,
                message='commented on your post',
                type=Notifications.NotificationType.COMMENTED.value
            )
        return value


class AnswerCommentModelSerializer(ModelSerializer):
    author = UserModelSerializer(many=False, read_only=True)

    class Meta:
        model = AnswerComment
        fields = ('content', 'author', 'answer')
        read_only_fields = ('created_at',)

    def update(self, instance, validated_data):
        old_content = instance.content
        new_content = validated_data.get('content', old_content)

        if new_content != old_content:
            validated_data['is_edited'] = True

        return super().update(instance, validated_data)


class ContributorSerializer(ModelSerializer):
    total_contributions = IntegerField()

    class Meta:
        model = User
        fields = ('id', 'username', 'total_contributions', 'avatar', 'full_name')


class CommunityStatsSerializer(Serializer):
    total_questions = IntegerField()
    active_users = IntegerField()
    answered_today = IntegerField()
    top_contributors = ContributorSerializer(many=True)


class SaveModelSerializer(ModelSerializer):
    class Meta:
        model = Save
        fields = ('id', 'blog', 'user')
        read_only_fields = ('id', 'user')

    def validate_blog(self, value):
        recipient = value.author
        sender = self.context["request"].user
        if sender != recipient:
            Notifications.objects.create(
                recipient=recipient,
                sender=sender,
                message='commented on your post',
                type=Notifications.NotificationType.SAVED.value
            )
        return value
