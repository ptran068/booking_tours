from django.db import models
from files.models import File
from users.models import CustomUser

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=50)
    parent_id = models.ForeignKey("self", related_name='categories', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Tours(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    views = models.IntegerField()
    images = models.ManyToManyField(File, related_name='image_tour', blank=True, null=True)
    videoID = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)
    address = models.TextField()
    price = models.FloatField()
    duration = models.CharField(max_length=100)
    quantityMembers = models.IntegerField()
    policy = models.TextField()
    createdBy = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title