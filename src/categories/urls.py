from django.urls import path
from . import views

urlpatterns = [
    path('', views.CategoryList.as_view()),
    path('create', views.PostCategoryList.as_view())
]
