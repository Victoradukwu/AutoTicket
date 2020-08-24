"""A module of custom application models"""
import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


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
    departure_date = models.DateField()
    departure_time = models.TimeField()
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


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    domain = os.getenv('DOMAIN')
    email_plain_text_message = f"{domain}/auth/reset-pw?token={reset_password_token.key}"
    send_mail(
        # title
        'Password reset for {title}'.format(title='Some website title'),
        # Message
        email_plain_text_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
