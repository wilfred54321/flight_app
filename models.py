from enum import unique
from flask_sqlalchemy import SQLAlchemy
import string
import random
from datetime import datetime, timedelta

db = SQLAlchemy()


class Flight(db.Model):
    __tablename__ = "flights"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, unique=True, nullable=False)
    origin = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    # duration = db.Column(db.Integer, nullable=False)
    # departure = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    # arrival = db.Column(db.Datetime, nullable=False, default=datetime.utcnow())
    passengers = db.relationship(
        "Passenger", backref="flights ", cascade="all, delete", lazy=True
    )
    # pilots= db.relationship("Pilot", backref = "flights", lazy = True)

    def add_passenger(self, firstname, lastname, gender, flight_id):
        # if not self.open_seats:
        #     return False

        passenger = Passenger(
            firstname=firstname, lastname=lastname, gender=gender, flight_id=self.id
        )
        db.session.add(passenger)
        db.session.commit()
        return passenger.booking_reference
        # return True

    def open_seats(self):
        return self.capacity - len(self.passengers)

    def delay_flight(self, amount):
        delay_amount = timedelta(minutes=amount)
        return self.arrival_time + delay_amount

    # def delete_flight(self):
    #     db.session.delete(self.id)
    #     db.session.commit()

    # db.session.add(new_arrival_time)
    # db.session.commit()


def generate_booking_reference():
    ref_data_set = string.ascii_uppercase
    selection = random.choices(ref_data_set, k=5)
    booking_reference = "".join(map(str, selection))
    return booking_reference


class Passenger(db.Model):
    __tablename__ = "passengers"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    booking_reference = db.Column(
        db.String, nullable=False, default=generate_booking_reference
    )
    flight_id = db.Column(db.Integer, db.ForeignKey("flights.id"), nullable=False)


def add_flight(code, origin, destination, capacity, departure_time, arrival_time):
    return Flight(
        code=code,
        origin=origin,
        destination=destination,
        capacity=capacity,
        departure_time=departure_time,
        arrival_time=arrival_time,
    )


def is_valid_flight_time(departure_time, arrival_time):
    if (
        departure_time >= datetime.now() + timedelta(hours=2)
        and arrival_time > departure_time
    ):
        return True
    return False


# class Pilot(db.Model):
#     __tablename__ = "pilots"
#     id = db.Column(db.Integer, primary_key = True)
#     firstname = db.Column(db.String, nullable = False)
#     lastname = db.Column(db.String,nullable = False)
#     flight_id = db.Column(db.Integer,db.ForeignKey("flights.id"),nullable = False)
