from django.urls import re_path
from .consumers import PostConsumer

url_patterns = [re_path(r"ws/post/(?P<post_id>[0-9a-f-]+)/$", PostConsumer.as_asgi())]
