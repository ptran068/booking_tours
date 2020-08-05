from django.db import models
from files.models import File
from users.models import CustomUser
from categories.models import Categories
import uuid


class Tours(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    views = models.IntegerField()
    images = models.ManyToManyField(File, related_name="image_tour", blank=True, null=True)
    video_id = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=300)
    amount = models.IntegerField()
    duration = models.DateTimeField()
    quantity_members = models.IntegerField()
    policy = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
