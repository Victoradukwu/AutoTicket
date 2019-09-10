"""A module of helper functions and classes"""
import os
from datetime import datetime, timedelta
from rest_framework_jwt.settings import api_settings
import cloudinary
import requests
from celery import shared_task
from django.core.mail import send_mail
from rest_framework.permissions import BasePermission, SAFE_METHODS
from apscheduler.schedulers.background import BackgroundScheduler
from django_filters import rest_framework as filters
from ..models import Ticket, Flight


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS \
               or (request.user.is_authenticated & request.user.is_staff)


class IsAdminUserOrOwnerReadOnly(BasePermission):
    """Admin has full access. Owner has read only"""
    def has_object_permission(self, request, view, obj):
        if obj.booked_by == request.user and request.method in SAFE_METHODS:
            return True
        return request.user.is_staff


class IsAdminUserOrOwnerReadAndUpdateOnly(BasePermission):
    """Admin has full access. Owner can only read and update"""
    def has_object_permission(self, request, view, obj):
        if obj == request.user and request.method in ['PUT', 'PATCH', 'GET']:
            return True
        return request.user.is_staff


def generate_token(user):
    """A helper function to generate token"""
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


def upload_image(image):
    cloudinary.config(
        cloud_name=os.getenv('CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET')
    )

    response = cloudinary.uploader.upload(image)
    return response['url']


def make_payment(payload):
    test_secret = os.getenv('PAYSTACK_TEST_SECRET_KEY')
    headers = {'Authorization': f'Bearer {test_secret}'}
    resp = requests.post('https://api.paystack.co/charge', json=payload, headers=headers)
    return resp.json()


@shared_task
def send_email(payload):
    send_mail(
        payload['subject'],
        payload['content'],
        'vicads01@gmail.com',
        [payload['email']],
        fail_silently=False
    )


def update_seat_status(seat, status):
    seat.status=status
    seat.save()


def send_reminders():
    """Send reminders to traveller who are travelling the next day"""
    next_day = (datetime.now() + timedelta(days=1)).date()
    tickets = Ticket.objects.filter(seat__flight__departure_time__date=next_day)
    for ticket in tickets:
        passenger = ticket.passenger
        flight_date = datetime.strftime(ticket.seat.flight.departure_time, '%Y-%m-%d %H:%M')
        flight_number = ticket.seat.flight.number
        seat_number = ticket.seat.seat_number
        email = ticket.booked_by.email
        mail_data = {
            'email': email,
            'subject': 'Travel Reminder',
            'content': f'Please be reminded of your schedulled flight as follows.\nPassenger: {passenger}\nDate & time: {flight_date}\nFlight no.: {flight_number}\nSeat no.: {seat_number}'
        }
        send_email.delay(mail_data)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_reminders, 'cron', hour=12, minute=0)
    scheduler.start()


class FlightFilter(filters.FilterSet):
    destination = filters.CharFilter(lookup_expr='icontains')
    departure = filters.CharFilter(lookup_expr='icontains')
    departure_time = filters.LookupChoiceFilter(field_name='departure_time', lookup_choices=[('exact', 'On'), ('gte', 'After'), ('lte', 'Before')])

    class Meta:
        model = Flight
        fields = ('destination', 'departure', 'departure_time', 'status',)


class TicketFilter(filters.FilterSet):
    passenger = filters.CharFilter(lookup_expr='icontains')
    booked_by = filters.CharFilter(field_name='booked_by__email', lookup_expr='icontains')
    flight_number = filters.CharFilter(field_name='seat__flight', lookup_expr='number__icontains')
    flight_date = filters.CharFilter(field_name='seat__flight', lookup_expr='departure_time__date')

    class Meta:
        model = Ticket
        fields = ('passenger', 'booked_by', 'flight_number', 'flight_date')
