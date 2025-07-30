from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from config.models import BaseModel, Timestamp


class AuthUser(BaseModel, AbstractBaseUser):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False, editable=False)
    username = models.EmailField(max_length=255, unique=True, null=False)
    phone_number = models.CharField(max_length=10)

    USERNAME_FIELD = "email"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)


class Post(BaseModel):
    caption = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images", null=True, blank=True)
    video = models.FileField(upload_to="videos", null=True, blank=True)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="posts")

    class Meta:
        ordering = ["-created_at"]


class Likes(Timestamp):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"], name="unique_like_per_user_post"
            )
        ]
        ordering = ["-created_at"]


class Comments(Timestamp):
    user = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=255, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"], name="unique_comment_per_user_post"
            )
        ]
        ordering = ["-created_at"]


class Shares(Timestamp):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="shares")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="shares")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"], name="unique_share_per_user_post"
            )
        ]
