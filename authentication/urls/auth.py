from django.urls import path

from authentication.views import *

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserGenericAPIView.as_view()),
    path('verify/code', VerifyCodeGenericAPIView.as_view()),
]

urlpatterns += [
    path('google/auth/', auth_google),
    path("auth/google/", GoogleAuthView.as_view(), name="google_auth"),
]
