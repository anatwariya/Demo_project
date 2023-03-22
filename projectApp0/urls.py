from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projectApp1/', include("projectApp1.urls")),
    path('projectApp2/', include("projectApp2.urls")),
    path('projectApp3/', include("projectApp3.urls")),
    path('projectMainApp/', include("projectMainApp.urls")),
]
