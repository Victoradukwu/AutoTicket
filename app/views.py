"""A module of app views"""
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.base_user import make_password, check_password
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, FlightSerializer, SeatSerializer, TicketSerializer
from .models import User, Flight, Seat
from .utils.helpers import generate_token, upload_image, send_email, make_payment, update_seat_status
from .utils.enums import SeatStatus, PaymentStatus


@api_view(['POST'])
def user_signup(request):
    data = request.data

    if data['password'] == data['confirm_password']:
        img = data['image']
        data['image'] = upload_image(img)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data['password'] =  make_password(data['password'])
            serializer.validated_data['username'] = serializer.validated_data['email']
            serializer.save()

            user = get_object_or_404(User, email=data['email'])
            token = generate_token(user)
            payload = {
                        'token': token,
                        'message': "Successfully signed up",
                        'user': serializer.data
                        }
            return Response(payload, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_signin(request):
    data = request.data
    user = get_object_or_404(User, email=data['email'])
    if check_password(data['password'], user.password):
        token = generate_token(user)
        payload = {
                    'token': token,
                    'message': "Successfully logged in",
                }
        return Response(payload, status=status.HTTP_200_OK)
    return Response({'message': 'Wrong password or email'}, status=status.HTTP_400_BAD_REQUEST)


class FlightList(generics.ListCreateAPIView):
    """A class view for creating a flight or getting a flight list"""
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class FlightDetail(generics.RetrieveUpdateDestroyAPIView):
    """A class view for single-flight operations: retrieve, delete, update"""

    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class SeatList(generics.ListCreateAPIView):
    """A class view for creating a seat object or getting a seat list"""
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


class SeatDetail(generics.RetrieveUpdateDestroyAPIView):
    """A class view for single-seat operations: retrieve, delete, update"""

    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


@api_view(['POST'])
def make_reservation(request):
    data = request.data
    if not data['email']:
        data['email'] = request.user.email
    serializer = TicketSerializer(data=data)
    if serializer.is_valid():
        serializer.validated_data['payment_status'] = PaymentStatus.pending
        seat = serializer.validated_data['seat']
        flight_date = datetime.strftime(seat.flight.departure_time, '%Y-%m-%d %H:%M')
        flight_number = seat.flight.number
        seat_number = seat.seat_number
        serializer.save()
        update_seat_status(seat, SeatStatus.booked)

        mail_data = {
            'email': data['email'],
            'subject': 'Ticket Reservation',
            'content': f'Reservation made\n date: {flight_date}\n flight no.: {flight_number}\n seat no.: {seat_number}'
        }
        send_email(mail_data)
        return Response({'message': 'Reservation successful. Details have been sent by email'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

