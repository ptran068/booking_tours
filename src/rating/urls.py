from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.RatingList.as_view()),
    path('update/<uuid:tour_id>', views.PutRating.as_view()),
    path('create', views.PostRating.as_view())
]
