from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from projectApp2.models import Car
from projectApp3.models import CarPart
from .models import User
from .serializer import UserSerializer
from django.conf import settings
from django.core.mail import send_mail

from .token import account_activation_token


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
        user = User(name=data["name"], username=data["username"], email=data["email"], password=data["password"])
        user.save()
        if data.get("user_cars",False):
            for car_id in data["user_cars"]:
                car = Car.objects.get(id=car_id)
                user.user_cars.add(car)
        user.save()
        serializer = UserSerializer(user)
        data = serializer.data
        user_id = urlsafe_base64_encode(force_bytes(data["id"]))
        token = account_activation_token.make_token(user)
        confirmation_link = f'http://127.0.0.1:8000/projectMainApp/user_email_confirmation/{user_id}/{token}/'
        subject = 'Welcome to Car-Part world'
        message = f'Hi {data["name"]},\nThank you for registering in Car-Part world.\n' \
                  f'Please click on this link for active your account.\n' \
                  f'{confirmation_link}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [data["email"], ]
        send_mail(subject, message, email_from, recipient_list)
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        data = request.data
        try:
            user = User.objects.get(pk=data["id"])
        except User.DoesNotExist:
            return Response({"message": f"User data not found with UserId:- {data['id']}"}, status=status.HTTP_204_NO_CONTENT)
        user.name = data["name"]
        user.username = data["username"]
        user.email = data["email"]
        user.password = data["password"]
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
        user.username = data.get("username", user.username)
        user.password = data.get("password", user.password)
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