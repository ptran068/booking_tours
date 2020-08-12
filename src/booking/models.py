from django.db import models
import uuid
from users.models import CustomUser
from tours.models import Tours


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    tours = models.ForeignKey(Tours, on_delete=models.CASCADE, related_name="tour")
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="user")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

