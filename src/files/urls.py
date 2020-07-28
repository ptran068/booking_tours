from django.urls import path
from .views import  UploadFile
from . import  views

urlpatterns = [
    path('upload', UploadFile.as_view()),
]
