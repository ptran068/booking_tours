
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tour/', include('tours.urls')),
    path('category/', include('categories.urls')),
    path('rating/', include('rating.urls')),
]

