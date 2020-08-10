from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'viewset', views.ReviewViewSet)

review_list = views.ReviewViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
review_detail = views.ReviewViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})


urlpatterns = [
    path('<uuid:pk>/like', views.like_review, name='like'),
    path('', review_list, name='review-list'),
    path('<uuid:pk>/', review_detail, name='review-detail'),
    path('manage/', views.ReviewByUser.as_view(), name='review-by-user')
]
