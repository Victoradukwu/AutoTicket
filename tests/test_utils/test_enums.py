"""Test module for enums module"""
from django.test import SimpleTestCase
from app.utils import enums


class TestEnums(SimpleTestCase):
    """Test class for testing custom Enum class"""

    def test_flightstatus_enum(self):
        """Testing the FlightStatus Enum"""
        flt_enum1 = enums.FlightStatus('1')
        flt_enum0 = enums.FlightStatus('0')

        self.assertEqual(flt_enum1.active, '1')
        self.assertEqual(flt_enum0.cancelled, '0')

    def test_seatstatus_enum(self):
        """Testing the SeatStatus Enum"""
        seat_enum1 = enums.SeatStatus('1')
        seat_enum0 = enums.SeatStatus('0')

        self.assertEqual(seat_enum1.available, '1')
        self.assertEqual(seat_enum0.booked, '0')

    def test_paymentstatus_enum(self):
        """Testing the PaymentStatus Enum"""
        pmt_enum1 = enums.PaymentStatus('paid')
        pmt_enum0 = enums.PaymentStatus('pending')

        self.assertEqual(pmt_enum1.paid, 'paid')
        self.assertEqual(pmt_enum0.pending, 'pending')


