"""A module of tests for flight views"""
from model_mommy import mommy
from django.test import TestCase, Client
from django.urls import reverse
from app.models import Flight


class TestFlightViews(TestCase):
    """Test class for Flight views"""

    def setUp(self):
        self.client = Client()
        self.auth_user = mommy.make('app.User', is_staff=True)
        self.client.force_login(self.auth_user)

    def test_flight_list_view(self):
        mommy.make('Flight', _quantity=8)

        resp = self.client.get(reverse('flight_list'))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 8)

    def test_flight_detail_view(self):
        flt = mommy.make('Flight')

        resp = self.client.get(reverse('flight_detail', args=[flt.id]))

        self.assertEqual(resp.status_code, 200)
        self.assertEquals(resp.data['departure'], flt.departure)

    def test_flight_creation_view(self):
        flt = mommy.prepare('Flight')
        data = {
            'departure':  flt.departure,
            'destination': flt.fare,
            'fare': flt.fare,
            'status': str(flt.status),
            'departure_time': flt.departure_time,
            'number': flt.number,
            'created_at':flt.created_at,
            'update_at': flt.updated_at
        }

        resp = self.client.post(reverse('flight_list'), data)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Flight.objects.first().status, flt.status)

    def test_flight_delete_view(self):
        flt = mommy.make('Flight')

        resp = self.client.delete(reverse('flight_detail', args=[flt.id]))
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Flight.objects.all().count(), 0)
