# delivery_management/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('vehicles.urls')),  # Include vehicles app URLs
]
