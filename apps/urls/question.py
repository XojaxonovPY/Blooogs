from django.urls import path

from apps.views import *

urlpatterns = [
    path('question-create', QuestionCreateAPIView.as_view()),
    path('questions', QuestionListAPIView.as_view()),
    path('question-delete/<int:pk>', QuestionDeleteAPIView.as_view()),
    path('question-update/<int:pk>', QuestionUpdateAPIView.as_view()),
    path('question-detail/<int:pk>', QuestionDetailAPIView.as_view()),
]

urlpatterns += [
    path('blog/like', LikeGenericAPIView.as_view()),
    path('blog/like/count/<int:pk>', LikeCountAPIView.as_view()),
    path('blog/like/remove', LikeRemoveAPIView.as_view()),

]

urlpatterns += [
    path('question/votes', QuestionVoteGenericAPIView.as_view()),
    path('question/count/votes/<int:pk>/', QuestionVoteCountAPIView.as_view()),
    path('question/remove/votes', QuestionVoteRemoveAPIView.as_view()),
]
