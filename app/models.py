"""A module of custom application models"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import enums


class User(AbstractUser):
    """Custom user class"""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100, null=False)
    image = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def repr(self):
        return f'{self.first_name} {self.last_name}'


class Flight(models.Model):
    """Flight model class"""

    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    fare = models.DecimalField(max_digits=6, decimal_places=2)
    number = models.CharField(max_length=20)
    departure_time = models.DateTimeField()
    status = models.CharField(
        max_length=1,
        choices=[(tag, tag.value) for tag in enums.FlightStatus],
        default=enums.FlightStatus.active)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def repr(self):
        return f'Flight No. {self.number}'


class Seat(models.Model):
    """A model class representing a particular seat on a particular flight"""

    seat_number = models.CharField(max_length=6)
    status = models.CharField(
        max_length=1,
        choices=[(tag, tag.value) for tag in enums.SeatStatus],
        default=enums.SeatStatus.available)
    flight = models.ForeignKey(Flight, related_name='seats', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def repr(self):
        return f'Seat no. {self.seat_number} on Flight No. {self.flight.number}'


class Ticket(models.Model):
    """A model class representing a passenger ticket"""

    passenger = models.CharField(max_length=50)
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE, primary_key=True,
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def repr(self):
        return f'Seat no. {self.seat_number} on Flight No. {self.flight.number}'

