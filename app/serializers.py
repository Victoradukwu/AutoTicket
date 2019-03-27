"""Module of serializers"""
from rest_framework import serializers

from .models import User, Flight, Ticket, Seat


class UserSerializer(serializers.ModelSerializer):
    """UserSerializer class"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'phone_number', 'image')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class FlightSerializer(serializers.ModelSerializer):
    """FlightSerializer class"""
    seats = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Flight
        fields = ('id', 'departure', 'destination', 'fare', 'status', 'number', 'departure_time', 'seats')


class SeatSerializer(serializers.ModelSerializer):
    """SeatSerializer class"""

    class Meta:
        model = Seat
        fields = ('id', 'status', 'seat_number', 'flight')


class TicketSerializer(serializers.ModelSerializer):
    """TicketSerializer class"""

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ('booked_by',)




