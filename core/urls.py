from django.urls import path
from .views import LikeView, CommentView, ShareView


urlpatterns = [
    path("like/", LikeView.as_view(), name="like_post"),
    path("comment/", CommentView.as_view(), name="comment_post"),
    path("share/", ShareView.as_view(), name="share_post"),
]
