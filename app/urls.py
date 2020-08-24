"""The module of urls for the app"""
from . import views
from django.urls import path, include
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('users/register/', views.RegisterView.as_view(), name='user_register'),
    path('users/login/', views.LoginView.as_view(), name='user_login'),
    path('users/social/<backend>/', views.exchange_token, name='social_auth'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('users/change-password/', views.PasswordChangeView.as_view(), name='password-change'),

    path('flights/', cache_page(30)(views.FlightList.as_view()), name='flight_list'),
    path('flights/<int:pk>/', views.FlightDetail.as_view(), name='flight_detail'),
    path('seats/', views.SeatList.as_view(), name='seat_list'),
    path('seats/<int:pk>/', views.SeatDetail.as_view(), name='seat_detail'),
    path('tickets/<int:pk>/', views.TicketDetail.as_view(), name='ticket_detail'),
    path('tickets/<flight>', views.FlightTicketList.as_view(), name='list_flight_ticket'),
    path('tickets/', views.TicketList.as_view(), name='list_ticket'),
   ]


