from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from projectApp2.models import Car
from projectApp3.models import CarPart
from .models import User
from .serializer import UserSerializer


class UserAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({"message": f"User data not found with UserId:- {pk}"}, status=status.HTTP_204_NO_CONTENT)
            serializer = UserSerializer(user)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        user = User(name=data["name"], email=data["email"])
        user.save()
        if data.get("user_cars",False):
            for car_id in data["user_cars"]:
                car = Car.objects.get(id=car_id)
                user.user_cars.add(car)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        data = request.data
        try:
            user = User.objects.get(pk=data["id"])
        except User.DoesNotExist:
            return Response({"message": f"User data not found with UserId:- {data['id']}"}, status=status.HTTP_204_NO_CONTENT)
        user.name = data["name"]
        user.email = data["email"]
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        data = request.data
        try:
            user = User.objects.get(pk=data["id"])
        except User.DoesNotExist:
            return Response({"message": f"User data not found with UserId:- {data['id']}"}, status=status.HTTP_204_NO_CONTENT)
        user.name = data.get("name", user.name)
        user.email = data.get("email", user.email)
        if data.get("user_cars", False):
            user.user_cars.clear()
            for car_id in data["user_cars"]:
                car = Car.objects.get(id=car_id)
                user.user_cars.add(car)
        if data.get("car_part_purchased", False):
            user.car_part_purchased.clear()
            for car_part_id in data["car_part_purchased"]:
                car_part = CarPart.objects.get(id=car_part_id)
                user.car_part_purchased.add(car_part)
        if data.get("car_part_added", False):
            user.car_part_added.clear()
            for car_part_id in data["car_part_added"]:
                car_part = CarPart.objects.get(id=car_part_id)
                user.car_part_added.add(car_part)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        if pk:
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({"message": f"User data not found with UserId:- {pk}"}, status=status.HTTP_204_NO_CONTENT)
            user.delete()
            return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Please provide an UserId."}, status=status.HTTP_400_BAD_REQUEST)