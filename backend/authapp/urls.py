from django.urls import path

from backend.authapp.reset_pwd import request_password_reset, reset_password
from .views import register, login, user_detail

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('user/', user_detail, name='user_detail'),
    path('request-password-reset/', request_password_reset, name='request_password_reset'),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset_password'),
]
