from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
import uuid

class CustomUser(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(('email address'), unique=True)
    phone = models.CharField(blank=True, null=True, max_length=15)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.email
