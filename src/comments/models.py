from django.db import models
import uuid
from users.models import CustomUser
from reviews.models import Review


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    reply_to = models.UUIDField(null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created_at']
