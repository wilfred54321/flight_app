from enum import unique
from flask_sqlalchemy import SQLAlchemy
from .utils import generate_booking_reference
from datetime import timedelta, datetime


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


def add_flight(code, origin, destination, capacity, departure_time, arrival_time):
    return Flight(
        code=code,
        origin=origin,
        destination=destination,
        capacity=capacity,
        departure_time=departure_time,
        arrival_time=arrival_time,
    )


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


class Pilot(db.Model):
    __tablename__ = "pilots"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    is_active = db.Column(db.Boolean, nullable=False, default=False)

   
     
