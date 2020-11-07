"""Test module for all urls"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from app.views import (
    FlightList,
    FlightDetail,
    SeatList,
    SeatDetail
)


class TestUrls(SimpleTestCase):
    """Test class for testing url resolutions"""

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
