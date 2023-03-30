import json

from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes

from django.conf import settings
from projectApp1.models import User
from projectApp1.serializer import UserSerializer
from projectApp1.token import account_activation_token
from projectApp1.views import UserAPIView
from projectApp2.models import Car
from projectApp2.serializer import CarSerializer
from projectApp3.models import CarPart
from projectApp3.serializer import CarPartSerializer
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password, make_password
from django.template import loader
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from validate_email_address import validate_email
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


@api_view(('GET',))
@permission_classes([IsAuthenticated])
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
@permission_classes([AllowAny])
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
@permission_classes([IsAuthenticated])
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


@api_view(('POST',))
@permission_classes([AllowAny])
def forget_password_reset(request, uid, token):
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
@permission_classes([AllowAny])
def send_forget_password_email(user):
    serializer = UserSerializer(user)
    data = serializer.data
    user_id = urlsafe_base64_encode(force_bytes(data["id"]))
    token = account_activation_token.make_token(user)
    confirmation_link = f'http://127.0.0.1:8000/car_world/forget_password_reset/{user_id}/{token}/'
    subject = 'Forget Password!'
    message = f'Hi {data["name"]},\nThis is the mail regarding your Forget Password request from Car-Part World ' \
              f'Portal.\n' \
              f'Please click on this link to reset the account password.\n' \
              f'{confirmation_link}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [data["email"], ]
    # send_mail(subject, message, email_from, recipient_list)


@api_view(('POST', 'GET'))
@permission_classes([AllowAny])
def forget_password(request, uid=None, token=None):
    if request.method == "POST":
        data = request.data
        if User.objects.filter(email=data["email_username"]).exists():
            user = User.objects.filter(email=data["email_username"]).first()
        elif User.objects.filter(username=data["email_username"]).exists():
            user = User.objects.filter(username=data["email_username"]).first()
        else:
            messages.error(request, "User Not exist with given Email/UserName")
            return render(request, "forget_password.html")
        send_forget_password_email(user)
        messages.success(request, "An Email has been sent to your account.")
        return render(request, 'redirect_page.html')
    return render(request, 'forget_password.html')


@api_view(('POST', 'GET',))
@permission_classes([IsAuthenticated])
def reset_password(request):
    if request.method == 'POST':
        data = request.data
        if User.objects.filter(username=data["username"]).exists():
            user = User.objects.filter(username=data["username"]).first()
        else:
            messages.error(request, "User Not exist with given UserName")
            return render(request, "reset_password_page.html")
        if not check_password(data['old_password'], user.password):
            messages.error(request, "Invalid Current Password.")
            return render(request, "reset_password_page.html")
        if data["new_password"] != data["confirm_password"]:
            messages.error(request, "Confirm Password does not match with New Password.")
            return render(request, "reset_password_page.html")
        user.password = make_password(data['new_password'])
        user.save()
        serializer = UserSerializer(user)
        data = serializer.data
        messages.success(request, "Password Changed.")
        return render(request, "redirect_page.html")
    return render(request, 'reset_password_page.html')


@api_view(('GET', 'POST',))
@permission_classes([AllowAny])
def signup(request):
    template = loader.get_template('signup_page.html')
    if request.method == 'POST':
        data = request.data
        if User.objects.filter(username=data["username"]).exists():
            messages.error(request, "UserName is already taken.")
            return render(request, 'signup_page.html')
        if User.objects.filter(email=data["email"]).exists():
            messages.error(request, "Email is already in use.")
            return render(request, 'signup_page.html')
        if not validate_email(data["email"]):
            messages.error(request, "Email doesn't exist.")
            return render(request, "signup_page.html")
        if data['password'] != data["confirm_password"]:
            messages.error(request, "Password and confirm password does not match.")
            return render(request, "signup_page.html")
        data = UserAPIView.as_view()(request._request)
        messages.success(request, "User registration is successful.")
        return redirect('redirect_to')
    return HttpResponse(template.render())


@api_view(('GET', 'POST'))
@permission_classes([AllowAny])
def home(request):
    car_parts = CarPart.objects.all()
    serializer = CarPartSerializer(car_parts, many=True)
    car_parts = json.dumps(serializer.data)
    car_parts = {"items": json.loads(car_parts)}
    return render(request, 'home_page.html', car_parts)


@api_view(('GET',))
@permission_classes([AllowAny])
def about_us(request):
    return render(request, 'about_us_page.html')


@api_view(('GET', 'POST'))
@permission_classes([AllowAny])
def contact_us(request):
    if request.method == 'POST':
        messages.success(request, "Thanks For Reaching Us out.")
        return render(request, 'redirect_page.html')
    return render(request, 'contact_us_page.html')


@api_view(('GET',))
@permission_classes([AllowAny])
def redirect_to(request):
    return render(request, 'redirect_page.html')


@api_view(('GET', 'POST'))
@permission_classes([IsAuthenticated])
def user_profile(request):
    if request.method == 'POST':
        request._request.method = "PATCH"
        user = UserAPIView.as_view()(request._request)
        messages.success(request, "Name Updated successfully.")
        return render(request, 'user_profile_page.html', user)
    data = {
        "user": {
            "name": "Ajay Kumar Natwariya",
            "username": "AAAAAAAA0",
            "email": "asdsaf@dgdfgv.com"
        }}
    return render(request, 'user_profile_page.html', data)


@api_view(('GET', 'POST',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@permission_classes([AllowAny])
def user_login(request):
    messages.set_level(request, 0)
    if request.method == 'POST':
        data = request.data
        if User.objects.filter(email=data["email_username"]).exists():
            user = User.objects.filter(email=data["email_username"]).first()
        elif User.objects.filter(username=data["email_username"]).exists():
            user = User.objects.filter(username=data["email_username"]).first()
        else:
            messages.error(request, "User doesn't exist with this Email/UserName.")
            return render(request, 'login_page.html')
        if not check_password(data['password'], user.password):
            messages.error(request, "Wrong Password.")
            return render(request, 'login_page.html')
        token = Token.objects.get_or_create(user=user)[0].key
        print(token)
        login(request, user)
        serializer = UserSerializer(user)
        data = serializer.data
        data["message"] = "user logged in"
        response = {"data": data, "token": token}
        return Response(response, template_name='home_page.html')
    return render(request, 'login_page.html')


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')
