from django.db import models
import uuid
from users.models import CustomUser
from files.models import File
from tours.models import Tours


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=20)
    images = models.ManyToManyField(File, null=True, blank=True)
    content = models.TextField()
    views = models.IntegerField(default=0, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="createdbyuser")
    tours = models.ForeignKey(Tours, on_delete=models.CASCADE)
    like = models.ManyToManyField(CustomUser, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
