from apps.urls.answer import urlpatterns as answer
from apps.urls.blog import urlpatterns as block
from apps.urls.comments import urlpatterns as comments
from apps.urls.question import urlpatterns as question

urlpatterns = [
    *answer,
    *block,
    *comments,
    *question,
]
