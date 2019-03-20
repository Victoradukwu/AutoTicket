"""The module of urls for the app"""
from .views import user_signup, user_signin
from django.urls import path

urlpatterns = [
    path('users/register/', user_signup, name='user_register'),
    path('users/login/', user_signin, name='user_login'),
   ]
