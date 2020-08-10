from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rating import views

router = DefaultRouter()
router.register(r'', views.RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
