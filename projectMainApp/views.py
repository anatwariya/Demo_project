from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes

from django.conf import settings
from projectApp1.models import User
from projectApp1.serializer import UserSerializer
from projectApp1.token import account_activation_token
from projectApp2.models import Car
from projectApp2.serializer import CarSerializer
from projectApp3.models import CarPart
from projectApp3.serializer import CarPartSerializer
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password, make_password
from django.template import loader
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

@api_view(('GET',))
def car_parts_filter_based_on_user(request, pk):
    car_parts = []
    user = User.objects.get(id=pk)
    user_serializer = UserSerializer(user)
    for user_car in user_serializer.data["user_cars"]:
        car_info = Car.objects.get(id=user_car["id"])
        car_serializer = CarSerializer(car_info)
        for car_part in car_serializer.data["parts_available"]:
            part_info = CarPart.objects.get(id=car_part)
            car_part_serializer = CarPartSerializer(part_info)
            car_parts.append(car_part_serializer.data)
    return Response({'car_parts': car_parts, 'total_count': len(car_parts)}, status=status.HTTP_200_OK)


@api_view(('GET',))
def user_email_confirmation(request, uid, token):
    try:
        pk = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(id=pk)
    except:
        return Response({'message': 'User Activation is not complete. Please login and send the activation link '
                                    'again. Thank you.'}, status=status.HTTP_200_OK)
    if user.active:
        return Response({"message": 'Email is already verified.'}, status=status.HTTP_200_OK)
    user.active = True
    user.save()
    user_serializer = UserSerializer(user)
    return Response({'message': 'Thank you for Confirming your Email.', 'user': user_serializer.data},
                    status=status.HTTP_200_OK)


@api_view(('GET',))
def send_user_confirmation_email(request, pk):
    user = User.objects.get(id=pk)
    if user.active:
        return Response({"message": 'Email is already verified.'}, status=status.HTTP_200_OK)
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
    return Response({"message": 'An Email has been sent to your registered EmailId.'}, status=status.HTTP_200_OK)


@api_view(('POST', 'GET', ))
def reset_password(request):
    data = request.data
    if User.objects.filter(username=data["username"]).exists():
        user = User.objects.filter(username=data["username"]).first()
    else:
        return Response({'message': f'No data found for Username:- {data["username"]}'},
                        status=status.HTTP_404_NOT_FOUND)
    if not check_password(data['old_password'], user.password):
        return Response({'message': 'Invalid Old Password.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    if data["new_password"] != data["confirm_password"]:
        return Response({'message': 'Confirm Password does not match.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    user.password = make_password(data['new_password'])
    user.save()
    serializer = UserSerializer(user)
    data = serializer.data
    return Response(data, status=status.HTTP_200_OK)


@api_view(('POST',))
def forget_password(request, uid, token):
    data = request.data
    if User.objects.filter(username=data["username"]).exists():
        user = User.objects.filter(username=data["username"]).first()
    else:
        return Response({'message': f'No data found for Username:- {data["username"]}'},
                        status=status.HTTP_404_NOT_FOUND)
    if data["new_password"] != data["confirm_password"]:
        return Response({'message': 'Confirm Password does not match.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    user.password = make_password(data['new_password'])
    user.save()
    serializer = UserSerializer(user)
    data = serializer.data
    return Response(data, status=status.HTTP_200_OK)


@api_view(('POST',))
def send_forget_password_email(request):
    data = request.data
    if User.objects.filter(username=data["username"]).exists():
        user = User.objects.filter(username=data["username"]).first()
    else:
        return Response({'message': f'No data found for Username:- {data["username"]}'},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    data = serializer.data
    user_id = urlsafe_base64_encode(force_bytes(data["id"]))
    token = account_activation_token.make_token(user)
    confirmation_link = f'http://127.0.0.1:8000/projectMainApp/forget_password/{user_id}/{token}/'
    subject = 'Forget Password!'
    message = f'Hi {data["name"]},\nThis is the mail regarding your Forget Password request from Car-Part World ' \
              f'Portal.\n' \
              f'Please click on this link to reset the account password.\n' \
              f'{confirmation_link}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [data["email"], ]
    send_mail(subject, message, email_from, recipient_list)
    return Response({"message": 'An Email has been sent to your registered EmailId.'}, status=status.HTTP_200_OK)


@api_view(('GET', 'POST',))
def login(request):
    template = loader.get_template('login_page.html')
    if request.method == 'POST':
        data = request.data
        if User.objects.filter(username=data["username"]).exists():
            user = User.objects.filter(username=data["username"]).first()
        else:
            return render(request, 'login_page.html')
        if not check_password(data['password'], user.password):
            return HttpResponse(template.render())
        serializer = UserSerializer(user)
        data = serializer.data
        return redirect('reset_password')
    return HttpResponse(template.render())


@api_view(('GET', 'POST',))
def signup(request):
    template = loader.get_template('signup_page.html')
    if request.method == 'POST':
        data = request.data
        return redirect('home')
    return HttpResponse(template.render())

@api_view(('GET',))
def home(request):
    template = loader.get_template('home_page.html')
    if request.method == 'POST':
        data = request.data
        if User.objects.filter(username=data["username"]).exists():
            user = User.objects.filter(username=data["username"]).first()
        else:
            messages.error(request, f'No data found for Username:- {data["username"]}')
            return render(request, 'login_page.html')
        if not check_password(data['password'], user.password):
            messages.error(request, 'Invalid username or Password.')
            return HttpResponse(template.render())
        serializer = UserSerializer(user)
        data = serializer.data
        return redirect('reset_password')
    return HttpResponse(template.render())