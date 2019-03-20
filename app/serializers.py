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

