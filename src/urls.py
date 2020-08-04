
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('tour/', include('tours.urls')),
    path('category/', include('categories.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('file/', include('files.urls')),

]
