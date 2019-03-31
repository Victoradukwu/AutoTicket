"""A module of tests for flight views"""
from model_mommy import mommy
from django.test import TestCase, Client
from django.urls import reverse
from app.models import Seat, Flight


class TestFlightViews(TestCase):
    """Test class for Seat views"""

    def setUp(self):
        self.client = Client()
        self.auth_user = mommy.make('app.User')
        self.client.force_login(self.auth_user)

    def test_seat_list_view(self):
        flt = mommy.make('Flight')
        mommy.make('Seat', _quantity=8, flight=flt)

        resp = self.client.get(reverse('seat_list'))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 8)

    def test_seat_detail_view(self):
        flt = mommy.make('Flight')
        seat = mommy.make('Seat', flight=flt)

        resp = self.client.get(reverse('seat_detail', args=[seat.id]))

        self.assertEqual(resp.status_code, 200)
        self.assertEquals(resp.data['status'], seat.status)

    def test_seat_creation_view(self):
        flt = mommy.make('Flight')
        seat = mommy.make('Seat', flight=flt)
        data = {
            'seat_number':  seat.seat_number[:2:],
            'status': str(seat.status),
            'flight': flt.id,
            'created_at': seat.created_at,
            'updated': seat.updated_at
        }

        resp = self.client.post(reverse('seat_list'), data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Seat.objects.first().status, seat.status)

    def test_seat_delete_view(self):
        flt = mommy.make('Flight')
        seat = mommy.make('Seat', flight=flt)

        resp = self.client.delete(reverse('seat_detail', args=[seat.id]))
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Seat.objects.all().count(), 0)

