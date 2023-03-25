from rest_framework.routers import DefaultRouter
from django.urls import path, include

from projectMainApp import views

urlpatterns = [
    path('car_parts_filter_based_on_user/<int:pk>/', views.car_parts_filter_based_on_user),
    path('user_email_confirmation/<uid>/<token>/', views.user_email_confirmation),
    path('send_user_confirmation_email/<int:pk>/', views.send_user_confirmation_email),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('forget_password/<uid>/<token>/', views.forget_password),
    path('send_forget_password_email/', views.send_forget_password_email),
]
