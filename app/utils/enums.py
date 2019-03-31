import enum


class FlightStatus(str, enum.Enum):
    active = '1'
    cancelled = '0'


class SeatStatus(str, enum.Enum):
    available = '1'
    booked = '0'

class PaymentStatus(str, enum.Enum):
    paid = 'paid'
    pending = 'pending'
