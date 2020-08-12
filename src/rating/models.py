from django.db import models
from users.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    tour_id = models.ForeignKey('tours.Tours', on_delete=models.CASCADE, blank=True)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('user_id', 'tour_id'))
        index_together = (('user_id', 'tour_id'))

