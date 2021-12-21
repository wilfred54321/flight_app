import string

import random
from datetime import datetime, timedelta


def generate_booking_reference():
    ref_data_set = string.ascii_uppercase
    selection = random.choices(ref_data_set, k=5)
    booking_reference = "".join(map(str, selection))
    return booking_reference

def generate_pilot_id():
    ref_data_set = string.digits
    selection = random.choices(ref_data_set,k=5)
    pilot_id = "".join(map(str,selection))
    return int(pilot_id) 

def generate_schedule_reference():
    ref_data_set = string.digits
    selection = random.choices(ref_data_set,k=8)
    schedule_reference = "".join(map(str,selection))
    return int(schedule_reference)

def generate_default_password():
    ref_data_set = string.digits +string.ascii_letters + ''.join(map(str,string.punctuation[0:6]))
    selection = random.choices(ref_data_set,k=7)
    default_password = "".join(map(str,selection))
    return str(default_password)

    
def is_valid_flight_time(departure_time, arrival_time):
    if (
        departure_time >= datetime.now() + timedelta(hours=2)
        and arrival_time > departure_time
    ):
        return True
    return False


def is_invalid_date_of_first_flight(date_of_first_flight):
    if date_of_first_flight > datetime.now() + timedelta(hours=1):
        return True
    return False

# function to format datetime for writing to database
def format_datetime(form_input):
    datetime_data = form_input.split("T")
    str_datetime_data = "".join(map(str, datetime_data))
    return datetime.strptime(str_datetime_data, "%Y-%m-%d%H:%M")



