"""The module of urls for the app"""
from .views import user_signup
from django.urls import path

urlpatterns = [
    path('users/register/', user_signup, name='user_register')
]
