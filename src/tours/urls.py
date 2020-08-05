from django.urls import path
from . import views

urlpatterns = [
    path('', views.ToursList.as_view()),
    path('<uuid:pk>', views.ToursListDetail.as_view()),
    path('edit/<uuid:pk>', views.EditOrDeleteToursDetail.as_view()),
    path('create', views.PostToursList.as_view(), name='post'),
]
