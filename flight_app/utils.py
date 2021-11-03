import string
import random
from datetime import datetime, timedelta


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
