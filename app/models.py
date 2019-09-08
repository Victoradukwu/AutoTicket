"""A module of custom application models"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user class"""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100, null=False)
    image = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, null=True)
    updated_at = models.DateTimeField(auto_now=True)


class Flight(models.Model):
    """Flight model class"""
    STATUS_CHOICES = [
        (1, 'active'),
        (0, 'cancelled')
    ]

    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    fare = models.DecimalField(max_digits=6, decimal_places=2)
    number = models.CharField(max_length=20)
    departure_time = models.DateTimeField()
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=1)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Seat(models.Model):
    """A model class representing a particular seat on a particular flight"""
    STATUS_CHOICES = [
        (1, 'available'),
        (0, 'booked')
    ]

    class Meta:
        unique_together = (('seat_number', 'flight'),)

    seat_number = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    flight = models.ForeignKey(Flight, related_name='seats', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Ticket(models.Model):
    """A model class representing a passenger ticket"""

    passenger = models.CharField(max_length=100)
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    booked_by = models.ForeignKey(User, related_name='tickets', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
