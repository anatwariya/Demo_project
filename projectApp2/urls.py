from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import CarGenericView

urlpatterns = [
    path('car/', CarGenericView.as_view())
]
