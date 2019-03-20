"""A module of helper functions and classes"""
import os
from rest_framework_jwt.settings import api_settings
import cloudinary


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