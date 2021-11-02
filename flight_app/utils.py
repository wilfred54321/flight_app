import string
import random
from datetime import datetime, timedelta
from flight_app.models import Passenger, Flight


def generate_booking_reference():
    ref_data_set = string.ascii_uppercase
    selection = random.choices(ref_data_set, k=5)
    booking_reference = "".join(map(str, selection))
    return booking_reference


def is_valid_flight_time(departure_time, arrival_time):
    if (
        departure_time >= datetime.now() + timedelta(hours=2)
        and arrival_time > departure_time
    ):
        return True
    return False


def add_flight(code, origin, destination, capacity, departure_time, arrival_time):
    return Flight(
        code=code,
        origin=origin,
        destination=destination,
        capacity=capacity,
        departure_time=departure_time,
        arrival_time=arrival_time,
    )
