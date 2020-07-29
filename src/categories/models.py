from django.db import models

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=50)
    parent_id = models.ForeignKey("self", related_name='categories', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
