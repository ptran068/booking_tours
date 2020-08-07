from django.urls import path
from . import views

urlpatterns = [
    path('', views.CommentList.as_view(), name="comment-list"),
    path('<uuid:pk>', views.CommentDetail.as_view(), name="comment-detail"),
]
