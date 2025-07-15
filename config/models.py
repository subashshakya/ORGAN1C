import uuid

from django.db import models

class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()


class BaseModel(Timestamp):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)