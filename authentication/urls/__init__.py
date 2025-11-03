from authentication.urls.auth import urlpatterns as auth
from authentication.urls.users import urlpatterns as users
from authentication.urls.follow_notification import urlpatterns as follow_notification

urlpatterns = [
    *auth,
    *users,
    *follow_notification
]
