"""A module of tests for flight views"""
from model_bakery import baker
from django.urls import reverse
from rest_framework.test import APITestCase

from app.models import Flight


class TestFlightViews(APITestCase):
    """Test class for Flight views"""

    def setUp(self):
        self.auth_user = baker.make('app.User', is_staff=True)
        self.client.force_login(self.auth_user)

    def test_flight_list_view(self):
        baker.make('Flight', _quantity=8)

        resp = self.client.get(reverse('flight_list'))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 8)

    def test_flight_detail_view(self):
        flt = baker.make('Flight')

        resp = self.client.get(reverse('flight_detail', args=[flt.id]))

        self.assertEqual(resp.status_code, 200)
        self.assertEquals(resp.data['departure'], flt.departure)

    def test_flight_creation_view(self):
        flt = baker.prepare('Flight')
        data = {
            'departure':  flt.departure,
            'destination': flt.fare,
            'fare': flt.fare,
            'status': flt.status,
            'departure_time': flt.departure_time,
            'departure_date': flt.departure_date,
            'number': flt.number,
            'created_at':flt.created_at,
            'update_at': flt.updated_at,
            'capacity': 10
        }
        resp = self.client.post(reverse('flight_list'), data, format='json')

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Flight.objects.first().status, flt.status)

    def test_flight_delete_view(self):
        flt = baker.make('Flight')

        resp = self.client.delete(reverse('flight_detail', args=[flt.id]))
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Flight.objects.all().count(), 0)
