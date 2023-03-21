from rest_framework import generics

from .models import Car
from .serializer import CarSerializer


class CarGenericView(generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
