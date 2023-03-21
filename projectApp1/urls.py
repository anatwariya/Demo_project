from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import UserAPIView

router = DefaultRouter()

urlpatterns = [
    path('user/', UserAPIView.as_view()),
    path('user/<int:pk>/', UserAPIView.as_view())
]
