from django.urls import path

from apps.views import *

urlpatterns = [
    path('answer-create', AnswerCreateAPIView.as_view()),
    path('answers', AnswerListAPIView.as_view()),
    path('answer-delete/<int:pk>', AnswerDeleteAPIView.as_view()),
    path('answer-update/<int:pk>', AnswerUpdateAPIView.as_view()),
    path('answer-detail/<int:pk>', AnswerDetailAPIView.as_view()),

]

urlpatterns += [
    path('answers/votes', AnswerVoteGenericAPIView.as_view()),
    path('answers/count/votes/<int:pk>/', AnswerVoteCountAPIView.as_view()),
    path('answers.remove/votes', AnswerVoteRemoveAPIView.as_view()),
]
