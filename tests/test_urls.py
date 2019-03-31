"""Test module for all urls"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from app.views import (
    user_signin,
    user_signup,
    make_reservation,
    payment,
    book_ticket,
    FlightList,
    FlightDetail,
    SeatList,
    SeatDetail
)


class TestUrls(SimpleTestCase):
    """Test class for testing url resolutions"""

    def test_user_signin_url_resolves(self):
        """Testing the user_signin url"""
        url = reverse('user_login')

        self.assertEqual(resolve(url).func, user_signin)
        self.assertEqual(resolve(url).url_name, 'user_login')

    def test_user_signup_url_resolves(self):
        """Testing the user_signup url"""
        url = reverse('user_register')

        self.assertEqual(resolve(url).func, user_signup)
        self.assertEqual(resolve(url).url_name, 'user_register')

    def test_reservation_resolves(self):
        """Testing the reservation url"""
        url = reverse('reservation')

        self.assertEqual(resolve(url).func, make_reservation)
        self.assertEqual(resolve(url).url_name, 'reservation')

    def test_payment_resolves(self):
        """Testing the payment url"""
        url = reverse('payment')

        self.assertEqual(resolve(url).func, payment)
        self.assertEqual(resolve(url).url_name, 'payment')

    def test_book_ticket_resolves(self):
        """Testing the book_ticket url"""
        url = reverse('book_ticket')

        self.assertEqual(resolve(url).func, book_ticket)
        self.assertEqual(resolve(url).url_name, 'book_ticket')

    def test_flight_list_url_resolves(self):
        """Testing the flight_list"""
        url = reverse('flight_list')

        self.assertEqual(resolve(url).func.view_class, FlightList)
        self.assertEqual(resolve(url).url_name, 'flight_list')

    def test_flight_detail_url_resolves(self):
        """Testing the flight-detail"""
        url = reverse('flight_detail', kwargs={'pk': 1})

        self.assertEqual(resolve(url).func.view_class, FlightDetail)
        self.assertEqual(resolve(url).url_name, 'flight_detail')

    def test_seat_list_url_resolves(self):
        """Testing the seat_list"""
        url = reverse('seat_list')

        self.assertEqual(resolve(url).func.view_class, SeatList)
        self.assertEqual(resolve(url).url_name, 'seat_list')

    def test_seat_detail_url_resolves(self):
        """Testing the seat-detail"""
        url = reverse('seat_detail', kwargs={'pk': 1})

        self.assertEqual(resolve(url).func.view_class, SeatDetail)
        self.assertEqual(resolve(url).url_name, 'seat_detail')