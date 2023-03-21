from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import CarPartViewSet

router = DefaultRouter()
router.register("car_part", CarPartViewSet, basename="car_parts")

urlpatterns = [
    path('', include(router.urls)),
]
