from django.urls import path
from . import views

urlpatterns = [
    path('', views.ToursList.as_view()),
    path('<int:pk>', views.ToursListDetail.as_view()),
    path('edit/<int:pk>', views.EditToursListDetail.as_view()),
    path('add/', views.PostToursList.as_view(), name='post'),
]