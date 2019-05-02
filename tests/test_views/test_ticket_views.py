"""A module of tests for ticket-related views"""
from model_mommy import mommy
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from urllib.parse import urlencode


class TestTicketViews(TestCase):
    """Test class for ticket-related activities views"""

    def setUp(self):
        self.client = Client()
        self.auth_user = mommy.make('app.User')
        self.client.force_login(self.auth_user)

    @patch('app.views.make_payment')
    def test_payments(self, mock_make_payment):
        mock_make_payment.return_value = {'data': {'status': 'success'}}
        data = urlencode({
            'email': 'bca@bca.bca',
            'amount': 1000,
            'pin': '0000',
            "number": 'number',
            "cvv": 222,
            "expiry_month": 12,
            "expiry_year":  20
        })

        resp = self.client.post(reverse('payment'), data, content_type="application/x-www-form-urlencoded")
        self.assertEqual(resp.status_code, 200)

    @patch('app.views.send_email')
    def test_make_reservations(self, mock_send_email):
        mock_send_email.return_value = None
        flight = mommy.make('Flight')
        seat = mommy.make('Seat', flight=flight)
        data = urlencode({
            'seat': seat.id,
            'email': 'xyz@xyz.xyc',
            'passenger': 'Duke'
        })

        resp = self.client.post(reverse('reservation'), data, content_type="application/x-www-form-urlencoded")
        self.assertEqual(resp.status_code, 200)

    @patch('app.views.send_email')
    def test_make_reservations_fail_without_passenger(self, mock_make_payment):
        mock_make_payment.return_value = None
        flight = mommy.make('Flight')
        seat = mommy.make('Seat', flight=flight)
        data = urlencode({
            'seat': seat.id,
            'email': 'xyz@xyz.xyc'
        })

        resp = self.client.post(reverse('reservation'), data, content_type="application/x-www-form-urlencoded")
        self.assertEqual(resp.status_code, 400)

    @patch('app.views.make_payment')
    @patch('app.views.send_email')
    def test_book_ticket(self, mock_send_mail, mock_make_payment):
        mock_make_payment.return_value = {'data': {'status': 'success'}}
        mock_send_mail.return_value = None
        flight = mommy.make('Flight')
        seat = mommy.make('Seat', flight=flight)
        data = urlencode({
                "passenger": "Dave",
                "seat": seat.id,
                "email": "vicads01@gmail.com",
                "pin": "1111",
                "number": "507850785078507812",
                "cvv": "081",
                "expiry_month": "12",
                "expiry_year":  "2020"
})

        resp = self.client.post(reverse('book_ticket'), data, content_type="application/x-www-form-urlencoded")
        self.assertEqual(resp.status_code, 200)

    @patch('app.views.make_payment')
    @patch('app.views.send_email')
    def test_book_ticket_fails_for_missing_passenger_field(self, mock_send_mail, mock_make_payment):
        mock_make_payment.return_value = {'data': {'status': 'success'}}
        mock_send_mail.return_value = None
        flight = mommy.make('Flight')
        seat = mommy.make('Seat', flight=flight)
        data = urlencode({
            "seat": seat.id,
            "email": "vicads01@gmail.com",
            "pin": "1111",
            "number": "507850785078507812",
            "cvv": "081",
            "expiry_month": "12",
            "expiry_year": "2020"
        })

        resp = self.client.post(reverse('book_ticket'), data, content_type="application/x-www-form-urlencoded")
        self.assertEqual(resp.status_code, 400)
