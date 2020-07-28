from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
import uuid
from files.models import File

class CustomUser(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(('email address'), unique=True)
    avatar = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(blank=True, null=True, max_length=15)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.email
        