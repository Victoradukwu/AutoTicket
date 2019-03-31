"""Test module for enums module"""
from django.test import TestCase
from model_mommy import mommy
from app.utils import helpers
from unittest.mock import patch


class TestHelpers(TestCase):
    """Test class for testing helper module"""

    def test_generate_token(self):
        """Testing the generate_token function"""
        usr = mommy.make('app.User')
        tkn = helpers.generate_token(usr)

        self.assertEqual(type(tkn), str)

    @patch('app.utils.helpers.cloudinary.uploader.upload')
    def test_upload_image(self, mock_upload):
        """Testing the upload_image function"""
        mock_upload.return_value = {'url': 'hhhhhhhhhhhh'}
        url = helpers.upload_image('qfqwfwfwe')

        self.assertEqual(type(url), str)

    @patch('app.utils.helpers.cloudinary.uploader.upload')
    def test_upload_image(self, mock_upload):
        """Testing the upload_image function"""
        mock_upload.return_value = {'url': 'hhhhhhhhhhhh'}
        url = helpers.upload_image('qfqwfwfwe')

        self.assertEqual(type(url), str)

    @patch('app.utils.helpers.requests.post')
    def test_make_payment(self, mock_post):
        """Testing the upload_image function"""

        helpers.make_payment({})

        mock_post.assert_called_once()


