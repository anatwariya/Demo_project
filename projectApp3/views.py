from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .models import CarPart
from .serializer import CarPartSerializer


class CarPartViewSet(viewsets.ViewSet):
    def list(self, request, pk=None):
        if pk:
            try:
                car_part = CarPart.objects.get(pk=pk)
            except CarPart.DoesNotExist:
                return Response({"message": f"CarPart data not found with CarPartId:- {pk}"}, status=status.HTTP_204_NO_CONTENT)
            serializer = CarPartSerializer(car_part)
        else:
            car_parts = CarPart.objects.all()
            serializer = CarPartSerializer(car_parts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        if pk:
            try:
                car_part = CarPart.objects.get(pk=pk)
            except CarPart.DoesNotExist:
                return Response({"message": f"CarPart data not found with CarPartId:- {pk}"}, status=status.HTTP_204_NO_CONTENT)
            serializer = CarPartSerializer(car_part)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Please provide an CarPartId."}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        data = request.data
        car_part = CarPart(car_part_name=data["car_part_name"], price=data["price"])
        car_part.save()
        serializer = CarPartSerializer(car_part)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        data = request.data
        try:
            car_part = CarPart.objects.get(pk=pk)
        except CarPart.DoesNotExist:
            return Response({"message": f"CarPart data not found with CarPartId:- {pk}"}, status=status.HTTP_204_NO_CONTENT)
        car_part.car_part_name = data["car_part_name"]
        car_part.price = data["price"]
        car_part.save()
        serializer = CarPartSerializer(car_part)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        data = request.data
        try:
            car_part = CarPart.objects.get(pk=pk)
        except CarPart.DoesNotExist:
            return Response({"message": f"CarPart data not found with CarPartId:- {pk}"}, status=status.HTTP_204_NO_CONTENT)
        car_part.car_part_name = data.get("car_part_name", car_part.car_part_name)
        car_part.price = data.get("price", car_part.price)
        car_part.save()
        serializer = CarPartSerializer(car_part)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        if pk:
            try:
                car_part = CarPart.objects.get(pk=pk)
            except CarPart.DoesNotExist:
                return Response({"message": f"CarPart data not found with CarPartId:- {pk}"}, status=status.HTTP_204_NO_CONTENT)
            car_part.delete()
            return Response({"message": "CarPart deleted successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Please provide an CarPartId."}, status=status.HTTP_400_BAD_REQUEST)
