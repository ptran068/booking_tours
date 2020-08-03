from django.contrib import admin
from .models import CustomUser

class UserAmin(admin.ModelAdmin):
    list_filter = ['email']
    search_fields = ['email']

admin.site.register(CustomUser, UserAmin)

