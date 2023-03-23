from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("projectApp1.urls")),
    path('cars', include("projectApp2.urls")),
    path('car_parts/', include("projectApp3.urls")),
    path('car_world/', include("projectMainApp.urls")),
]