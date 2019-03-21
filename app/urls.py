"""The module of urls for the app"""
from . import views
from django.urls import path

urlpatterns = [
    path('users/register/', views.user_signup, name='user_register'),
    path('users/login/', views.user_signin, name='user_login'),
    path('flights/', views.FlightList.as_view(), name='flight_list'),
    path('flights/<int:pk>/', views.FlightDetail.as_view(), name='flight_detail'),
    path('seats/', views.SeatList.as_view(), name='seat_list'),
    path('seats/<int:pk>/', views.SeatDetail.as_view(), name='seat_detail'),
    path('flights/reservation/', views.make_reservation, name='reservation'),
   ]
