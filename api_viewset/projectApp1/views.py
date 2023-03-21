from django.db.utils import IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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