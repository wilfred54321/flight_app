
from datetime import date

from flight_app.utils import generate_booking_reference,datetime,timedelta,format_datetime
from flight_app import db

import flight_app


class Flight(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    model = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    date_of_first_flight = db.Column(db.DateTime, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    schedules = db.relationship(
        "Schedule", backref="flight", cascade="all,delete", lazy='subquery'
    )

    def status(self):
        if self.is_available == False:
            return "unavailable"
        return "available"


    def enable(self):
        self.is_available = True
        db.session.commit()
        return self.is_available

    def disable(self):
        self.is_available = False
        db.session.commit()
        return self.is_available

    
    def schedule_flight(self, origin, destination,capacity,departure_time, arrival_time):
        schedule = Schedule(
            flight_id = self.id,
            origin=origin,
            destination=destination,
            capacity = capacity,
            departure_time=departure_time,
            arrival_time=arrival_time
        )
        db.session.add(schedule)
        db.session.commit()
        return schedule

    # duration = db.Column(db.Integer, nullable=False)
    # departure = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    # arrival = db.Column(db.Datetime, nullable=False, default=datetime.utcnow())

    # pilots= db.relationship("Pilot", backref = "flights", lazy = True)


class Schedule(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    timestamp = db.Column(db.DateTime, nullable = False, default = datetime.now)
    status = db.Column(db.String(30), nullable=False,default = 'available')

    flight_id = db.Column(db.Integer, db.ForeignKey("flight.id"))

    passengers = db.relationship(
        "Passenger", backref="schedule ", cascade="all, delete", lazy=True
    )
    pilots = db.relationship("Pilot",backref = "schedule", cascade = "all,delete", lazy = True)

    @property
    def add_passenger(self, firstname, lastname, gender, flight_id):
        # if not self.open_seats:
        #     return False

        passenger = Passenger(
            firstname=firstname, lastname=lastname, gender=gender, schedule_id=self.id
        )
        db.session.add(passenger)
        db.session.commit()
        return passenger.booking_reference
        # return True

    @property
    def open_seats(self):
        return self.capacity - len(self.passengers)

    @property
    def delay_flight(self, amount):
        delay_amount = timedelta(minutes=amount)
        return self.arrival_time + delay_amount


    def duration(self):
        self.arrival_time - self.departure_time
        
        



class Passenger(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)
    booking_reference = db.Column(
        db.String, nullable=False, default=generate_booking_reference
    )
    schedule_id = db.Column(db.Integer, db.ForeignKey("schedule.id"))


class Pilot(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    is_available = db.Column(db.Boolean, nullable=False, default=True)
    schedule_id = db.Column(db.Integer,db.ForeignKey('schedule.id'))


    def status(self):
        if self.is_available == False:
            return "unavailable"
        return "available"

    def enable(self):
        self.is_available = True
        db.session.commit()
        return self.is_available

    def disable(self):
        self.is_available = False
        db.session.commit()
        return self.is_available
