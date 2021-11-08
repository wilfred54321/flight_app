
from datetime import date

from flight_app.utils import generate_booking_reference,datetime, generate_pilot_id, generate_schedule_reference,timedelta,format_datetime
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
    reference = db.Column(db.Integer, unique = True , nullable = False, default = generate_schedule_reference)

    flight_id = db.Column(db.Integer, db.ForeignKey("flight.id"))

    passengers = db.relationship(
        "Passenger", backref="schedule ", cascade="all, delete", lazy='subquery'
    )
    

    
    def add_passenger(self, firstname, lastname, gender,email):
        # if not self.open_seats:
        #     return False
        passenger = Passenger(
            firstname=firstname, lastname=lastname, gender=gender,email = email,schedule_id = self.id
        )
        db.session.add(passenger)
        db.session.commit()
        return passenger.booking_reference
        # return True

    # def add_pilot(self,firstname,lastname,email,gender,category,level):
    #     pilot = Pilot(firstname = firstname,lastname = lastname, email = email,gender = gender,category = category,level=level,schedule_id = self.id)
    #     db.session.add(pilot)
    #     db.session.commit()

    def open_seats(self):
        return self.capacity - len(self.passengers)
    
    def delay_flight(self,amount):
        new_arrival_time = self.arrival_time + timedelta(minutes=amount)
        self.arrival_time = new_arrival_time
        db.session.commit()
        return self.arrival_time

    def time_to_departure(self):
        ttd = self.departure_time - datetime.now()
        return round(((ttd.total_seconds())/60),2)

    def expected_arrival_time(self):
        eta = self.arrival_time - datetime.now()
        return round(((eta.total_seconds())/60),2)

    def arrived(self):
        if self.expected_arrival_time == 0:
            self.status = 'arrived'
        db.session.commit()

       
        
        


    def duration(self):
        duration = self.arrival_time - self.departure_time
        return duration

        
        



class Passenger(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable = False)
    is_checked_in = db.Column(db.Boolean, default = False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)
    booking_reference = db.Column(
        db.String, nullable=False, default=generate_booking_reference
    )
    schedule_id = db.Column(db.Integer, db.ForeignKey("schedule.id"))


    def status(self):
        if self.is_checked_in == False:
            return "not checked in"
        return "checked in"

scheduled_pilots = db.Table('scheduled_pilots',
db.Column('pilot_id',db.Integer,db.ForeignKey('pilot.id')),
db.Column('schedule_id',db.Integer,db.ForeignKey('schedule.id')))


class Pilot(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, unique = True,default = generate_pilot_id)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(30), nullable=False, default = "regular")
    level = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    is_available = db.Column(db.Boolean, nullable=False, default=True)
    schedules = db.relationship('Schedule',secondary = 'scheduled_pilots',backref =db.backref('schedules',lazy = 'dynamic'))
    
    


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
