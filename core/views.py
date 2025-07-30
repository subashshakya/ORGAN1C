from django.db import IntegrityError, transaction
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from .models import Likes, Comments, Shares
from .decorators import validate_post


class LikeView(GenericAPIView):
    @validate_post
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        user = self.request.user
        post_id = request.data.get("post_id")
        try:
            likes_exist = Likes.objects.get(user=user.id, post=post_id)
            likes_exist.delete()
            return Response({"status": HTTP_204_NO_CONTENT})
        except Likes.DoesNotExist:
            try:
                Likes.objects.create(user=user.id, post=post_id)
                return Response({"status": HTTP_201_CREATED})
            except IntegrityError:
                return Response(
                    {
                        "status": HTTP_400_BAD_REQUEST,
                        "message": "Integrity error for likes",
                    }
                )
            except Exception as e:
                return Response(
                    {
                        "status": HTTP_500_INTERNAL_SERVER_ERROR,
                        "message": "Internal server error",
                        "error": str(e),
                    }
                )


class CommentView(GenericAPIView):
    @validate_post
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        user = self.request.user
        post_id = request.data.get("post_id")
        comment = request.data.get("comment")
        if not comment:
            return Response(
                {"status": HTTP_400_BAD_REQUEST, "message": "Comment on post is blank"}
            )
        try:
            Comments.objects.create(user=user.id, post=post_id, comment=comment)
            return Response(
                {
                    "status": HTTP_201_CREATED,
                }
            )
        except Exception as e:
            return Response(
                {
                    "status": HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "Internal server error",
                    "error": str(e),
                }
            )


class ShareView(GenericAPIView):
    @validate_post
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        user = self.request.user
        post_id = request.data.get("post_id")
        try:
            Shares.objects.create(user=user.id, post=post_id)
            return Response(
                {
                    "status": HTTP_201_CREATED,
                }
            )
        except Exception as e:
            return Response(
                {
                    "status": HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "Internal server error",
                    "error": str(e),
                }
            )
