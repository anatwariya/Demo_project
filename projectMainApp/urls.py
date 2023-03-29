from rest_framework.routers import DefaultRouter
from django.urls import path, include

from projectMainApp import views

urlpatterns = [
    path('car_parts_filter_based_on_user/<int:pk>/', views.car_parts_filter_based_on_user),
    path('user_email_confirmation/<uid>/<token>/', views.user_email_confirmation),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('forget_password/<uid>/<token>/', views.forget_password_reset),
    path('send_forget_password_email/', views.send_forget_password_email),
    path('forget_password/', views.forget_password, name="forget_password"),
    path('about_us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('redirect_to/', views.redirect_to, name='redirect_to'),
    path('user_profile/', views.user_profile, name='user_profile'),
]
