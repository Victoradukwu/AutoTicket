"""A module of app views"""
from django.shortcuts import get_object_or_404
from django.contrib.auth.base_user import make_password, check_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from .utils.helpers import generate_token, upload_image


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
