from ckeditor.fields import RichTextField
from django.db.models import ImageField, DateTimeField, Model, ForeignKey, CASCADE, ManyToManyField
from django.db.models.fields import CharField, BooleanField


class Blog(Model):
    author = ForeignKey('authentication.User', related_name='blogs', on_delete=CASCADE)
    title = CharField(max_length=255)
    content = RichTextField()
    tags = CharField(max_length=255)
    likes = ManyToManyField('authentication.User', related_name='blog_likes')
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BlogView(Model):
    class Meta:
        unique_together = ('blog', 'user')

    user = ForeignKey('authentication.User', on_delete=CASCADE, related_name='blog_views')
    blog = ForeignKey('apps.Blog', on_delete=CASCADE, related_name='blog_views')
    viewed_at = DateTimeField(auto_now=True)


class BlogImages(Model):
    blog = ForeignKey('apps.Blog', on_delete=CASCADE, related_name='images')
    image = ImageField()


class Comment(Model):
    blog = ForeignKey('apps.Blog', on_delete=CASCADE, related_name="comments")
    author = ForeignKey('authentication.User', on_delete=CASCADE)
    content = RichTextField()
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username}"


class Question(Model):
    author = ForeignKey('authentication.User', on_delete=CASCADE, related_name="questions")
    title = CharField(max_length=255)
    content = RichTextField()
    created_at = DateTimeField(auto_now_add=True)
    votes = ManyToManyField('authentication.User', related_name='question_votes')
    is_edited = BooleanField(default=False)

    def __str__(self):
        return self.title


class QuestionView(Model):
    class Meta:
        unique_together = ('question', 'user')

    question = ForeignKey('apps.Question', on_delete=CASCADE, related_name="question_views")
    user = ForeignKey('authentication.User', on_delete=CASCADE, related_name="question_views")
    viewed_at = DateTimeField(auto_now=True)


class Answer(Model):
    question = ForeignKey('apps.Question', on_delete=CASCADE, related_name="answers")
    author = ForeignKey('authentication.User', on_delete=CASCADE, related_name="answers")
    content = RichTextField()
    created_at = DateTimeField(auto_now_add=True)
    upvotes = ManyToManyField('authentication.User', related_name="upvoted_answers", blank=True)
    downvotes = ManyToManyField('authentication.User', related_name="downvoted_answers", blank=True)
    is_edited = BooleanField(default=False)

    def __str__(self):
        return f"Answer by {self.author.username}"


class AnswerView(Model):
    class Meta:
        unique_together = ('answer', 'user')

    answer = ForeignKey('apps.Answer', on_delete=CASCADE, related_name="answer_views")
    user = ForeignKey('authentication.User', on_delete=CASCADE, related_name="answer_views")
    viewed_at = DateTimeField(auto_now=True)


class AnswerComment(Model):
    author = ForeignKey('authentication.User', on_delete=CASCADE, related_name="comments")
    content = RichTextField()
    answer = ForeignKey('apps.Answer', on_delete=CASCADE, related_name="comments")
    created_at = DateTimeField(auto_now_add=True)
    is_edited = BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.author.username}"


class Save(Model):
    user = ForeignKey('authentication.User', on_delete=CASCADE, related_name='saves')
    blog = ForeignKey('apps.Blog', on_delete=CASCADE, related_name='saves')
