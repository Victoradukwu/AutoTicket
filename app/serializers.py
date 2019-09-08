"""Module of serializers"""
from rest_framework import serializers

from .models import User, Flight, Ticket, Seat


class UserSerializer(serializers.ModelSerializer):
    """UserSerializer class"""

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'image')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class SeatSerializer(serializers.ModelSerializer):
    """SeatSerializer class"""

    class Meta:
        model = Seat
        fields = ('id', 'status', 'seat_number', 'flight')


class FlightSerializer(serializers.ModelSerializer):
    """FlightSerializer class"""
    seats = SeatSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = ('id', 'departure', 'destination', 'fare', 'status', 'number', 'departure_time', 'seats')


class TicketSerializer(serializers.ModelSerializer):
    """TicketSerializer class"""
    seat = SeatSerializer(read_only=True)
    booked_by = UserSerializer(read_only=True)
    passenger = serializers.CharField(write_only=True)
    flight = serializers.CharField(write_only=True)
    pin = serializers.CharField(write_only=True)
    number = serializers.CharField(write_only=True)
    cvv = serializers.CharField(write_only=True)
    expiry_month = serializers.CharField(write_only=True)
    expiry_year = serializers.CharField(write_only=True)

    class Meta:
        model = Ticket
        fields = ('__all__')
        read_only_fields = ('booked_by', 'seat')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)
    confirm_password = serializers.CharField(max_length=200)
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    phone_number = serializers.CharField(max_length=200)
    image = serializers.ImageField()


class ReservationSerializer(serializers.Serializer):
    seat = serializers.IntegerField()
    passenger = serializers.CharField(max_length=200)


class BookingSerializer(serializers.Serializer):
    email = serializers.EmailField()
    passenger = serializers.CharField(max_length=200)
    seat = serializers.IntegerField()
    pin = serializers.CharField(max_length=200)
    number = serializers.CharField(max_length=200)
    cvv = serializers.CharField(max_length=200)
    expiry_month = serializers.CharField(max_length=200)
    expiry_year = serializers.CharField(max_length=200)


class PaymentSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    amount = serializers.DecimalField(max_digits=9, decimal_places=2)
    pin = serializers.CharField(max_length=200)
    number = serializers.CharField(max_length=200)
    cvv = serializers.CharField(max_length=200)
    expiry_month = serializers.CharField(max_length=200)
    expiry_year = serializers.CharField(max_length=200)
