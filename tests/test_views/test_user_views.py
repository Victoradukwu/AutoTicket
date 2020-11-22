"""A module of tests for flight views"""
from model_bakery import baker
from django.urls import reverse
from unittest.mock import patch
from django.contrib.auth.base_user import make_password
from rest_framework.test import APITestCase


class TestUserViews(APITestCase):
    """Test class for User views"""

    def setUp(self):
        self.auth_user = baker.make('app.User')
        self.client.force_login(self.auth_user)

    @patch('app.views.upload_image')
    def test_user_signup_fail_for_wrong_confirm_password(self, mock_upload_image):
        user = baker.prepare('app.User')
        mock_upload_image.return_value = 'kkkhggghhfffg'
        data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'password': user.password,
            'confirm_password': 'another_password',
            'image': user.image,
            'phone_number': user.phone_number,
            'updated_at': user.updated_at
        }

        resp = self.client.post(reverse('user_register'), data)
        self.assertEqual(resp.status_code, 400)

    @patch('app.views.upload_image')
    def test_user_signup_fail_for_missing_email(self, mock_upload_image):
        user = baker.prepare('app.User')
        mock_upload_image.return_value = 'kkkhggghhfffg'
        data = {
            'first_name': user.first_name,
            'last_name': 100,
            'email': 'ewqwefwe',
            'password': user.password,
            'confirm_password': user.password,
            'image': user.image,
            'phone_number': user.phone_number,
            'updated_at': user.updated_at
        }

        resp = self.client.post(reverse('user_register'), data)
        self.assertEqual(resp.status_code, 400)

    @patch('app.views.upload_image')
    def test_user_signup_view(self, mock_upload_image):
        user = baker.prepare('app.User')
        mock_upload_image.return_value = 'kkkhggghhfffg'
        data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'password': user.password,
                'confirm_password': user.password,
                'image': user.image,
                'phone_number': user.phone_number,
                'updated_at': user.updated_at
        }

        resp = self.client.post(reverse('user_register'), data, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['message'], 'Successfully signed up')

    def test_user_signin_fail_for_wrong_password(self):
        user = baker.make('app.User')
        data = {
            'email': user.email,
            'password': 'wrong_password',

        }

        resp = self.client.post(reverse('user_login'), data)
        self.assertEqual(resp.status_code, 400)

    def test_user_signin_passes(self):
        user = baker.make('app.User', password=make_password('password'))
        data = {
            'email': user.email,
            'password': 'password',
        }

        resp = self.client.post(reverse('user_login'), data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['message'], 'Successfully logged in')



