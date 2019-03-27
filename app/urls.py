"""The module of urls for the app"""
from . import views
from django.urls import path

urlpatterns = [
    path('users/register/', views.user_signup, name='user_register'),
    path('users/login/', views.user_signin, name='user_login'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('flights/', views.FlightList.as_view(), name='flight_list'),
    path('flights/<int:pk>/', views.FlightDetail.as_view(), name='flight_detail'),
    path('seats/', views.SeatList.as_view(), name='seat_list'),
    path('seats/<int:pk>/', views.SeatDetail.as_view(), name='seat_detail'),
    path('tickets/<int:pk>/', views.TicketDetail.as_view(), name='ticket_detail'),
    path('tickets/reservation/', views.make_reservation, name='reservation'),
    path('tickets/book/', views.book_ticket, name='book_ticket'),
    path('tickets/list/<flight>', views.TicketList.as_view(), name='list_ticket'),
    path('payment/', views.payment, name='payment'),
   ]
