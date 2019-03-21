"""A module of helper functions and classes"""
import os
from rest_framework_jwt.settings import api_settings
import cloudinary
import requests
from django.core.mail import send_mail
import json


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
