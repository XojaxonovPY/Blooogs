from django.urls import path

from apps.views import *

# comment
urlpatterns = [
    path('commnet', CommentCreateAPIView.as_view()),
    path('commnet/list/<int:pk>', CommentListAPIView.as_view()),
    path('commnet/delete/<int:pk>', CommentDestroyAPIView.as_view()),
    path('comment', CommentCreateAPIView.as_view()),
    path('comment/list/<int:pk>', CommentListAPIView.as_view())
]

# answer's comment
urlpatterns += [
    path('answer-comment-create', AnswerCommentCreateAPIView.as_view()),
    path('answer-commnet-update/<int:pk>', AnswerCommentUpdateAPIView.as_view()),
    path('answer-commnet-delete/<int:pk>', AnswerCommentDeleteAPIView.as_view()),
    path('answer-comments', AnswerCommentListAPIView.as_view()),

]

# statistics
urlpatterns += [
    path('community-stats/', CommunityStatsView.as_view(), name='community-stats'),
]
