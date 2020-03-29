from django.test import TestCase
from app.models import Flight
from model_mommy import mommy


class TestFlightModel(TestCase):

    def test_can_create_flight(self):
        flight = mommy.prepare('Flight')
        Flight.objects.create(
            departure=flight.departure,
            destination=flight.destination,
            fare=flight.fare,
            number=flight.number,
            departure_time=flight.departure_time,
            departure_date=flight.departure_date,
            status=flight.status,
            created_at=flight.created_at,
            updated_at=flight.updated_at
        )

        self.assertEqual(Flight.objects.all().count(), 1)
        self.assertIsInstance(Flight.objects.get(pk=1), Flight)
        self.assertEqual(Flight.objects.get(pk=1).status, flight.status)

    def test_can_retrieve_flights(self):
        mommy.make('Flight', _quantity=10)

        flights = Flight.objects.all()

        self.assertEqual(flights.count(), 10)

    def test_can_update_flight(self):
        mommy.make('Flight')

        flight = Flight.objects.first()
        flight.departure = 'Abuja'
        flight.save()

        self.assertEqual(Flight.objects.get(pk=13).departure, 'Abuja')

    def test_can_delete_flights(self):
        mommy.make('Flight')

        flt = Flight.objects.first()
        flt.delete()

        with self.assertRaises(Flight.DoesNotExist):
            Flight.objects.get(number=flt.number)
