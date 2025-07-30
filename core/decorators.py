from functools import wraps
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from .models import Post


def validate_post(view_func):
    @wraps(view_func)
    def wrapped_view_func(self, request, *args, **kwargs):
        req_data = self.request.data
        if not req_data:
            return Response(
                {"status": HTTP_400_BAD_REQUEST, "message": "No request data found"}
            )
        post_id = req_data.get("post_id")
        if not post_id:
            return Response(
                {"status": HTTP_400_BAD_REQUEST, "message": "Post id is required"}
            )
        if Post.objects.filter(pk=post_id).exists():
            return view_func(self, request, *args, **kwargs)
        else:
            return Response(
                {
                    "status": HTTP_400_BAD_REQUEST,
                    "message": "Please provide a valid post",
                }
            )

    return wrapped_view_func
