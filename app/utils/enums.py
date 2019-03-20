import enum


class FlightStatus(str, enum.Enum):
    active = '1'
    cancelled = '0'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class SeatStatus(str, enum.Enum):
    available = '1'
    booked = '0'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)