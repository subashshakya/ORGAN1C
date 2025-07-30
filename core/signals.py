from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.db import models
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Likes, Comments, Shares
from config.enums import PostUpdateType


@receiver(post_save, sender=Likes)
def post_liked(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        post.likes_count = models.F("likes_count") + 1
        post.refresh_from_db()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"post_{instance.post.id}",
            {
                "type": "post_update",
                "post_id": instance.post.id,
                "likes_count": instance.post.likes_count,
                "from": PostUpdateType.LIKED,
            },
        )


@receiver(post_save, sender=Comments)
def post_commented(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        post.comments_count = models.F("comments_count") + 1
        post.refresh_from_db()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"post_{instance.post.id}",
            {
                "type": "post_update",
                "post_id": instance.post.id,
                "comments_count": instance.post.comments_count,
                "from": PostUpdateType.COMMENTED,
            },
        )


@receiver(post_save, sender=Shares)
def post_shared(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        post.shares_count = models.F("shares_count") + 1
        post.refresh_from_db()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"post_{instance.post.id}",
            {
                "type": "post_update",
                "post_id": instance.post.id,
                "shares_count": instance.post.shares_count,
                "from": PostUpdateType.SHARED,
            },
        )


@receiver(post_delete, sender=Likes)
def post_like_removed(sender, instance, **kwargs):
    post = instance.post
    post.likes_count = models.F("likes_count") - 1
    post.refresh_from_db()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"post_{instance.post.id}",
        {
            "type": "post_update",
            "post_id": instance.post.id,
            "likes_count": instance.post.likes_count,
            "from": PostUpdateType.LIKED,
        },
    )


@receiver(post_delete, sender=Comments)
def post_comment_removed(sender, instance, **kwargs):
    post = instance.post
    post.comments_count = models.F("comments_count") - 1
    post.refresh_from_db()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"post_{instance.post.id}",
        {
            "type": "post_update",
            "post_id": instance.post.id,
            "comments_count": instance.post.comments_count,
            "from": PostUpdateType.COMMENTED,
        },
    )
