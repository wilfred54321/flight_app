from flask_sqlalchemy import SQLAlchemy
db =SQLAlchemy()


class Flight(db.Model):
    __tablename__ = "flights"
    id = db.Column(db.Integer,primary_key = True)
    code = db.Column(db.String, nullable = False)
    origin = db.Column(db.String,nullable = False)
    destination = db.Column(db.String,nullable = False)
    capacity = db.Column(db.Integer,nullable = False)
    duration = db.Column(db.Integer,nullable = False)
    passengers= db.relationship("Passenger", backref = "flights", lazy = True)
    pilots= db.relationship("Pilot", backref = "flights", lazy = True)
    



class Passenger(db.Model):
    __tablename__ = "passengers"
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String, nullable = False)
    lastname = db.Column(db.String, nullable = False)
    Gender = db.Column(db.String, nullable = False)
    flight_id = db.Column(db.Integer, db.ForeignKey("flights.id"), nullable = False)



class Pilot(db.Model):
    __tablename__ = "pilots"
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String, nullable = False)
    lastname = db.Column(db.String,nullable = False)
    id_number = db.Column(db.Integer,db.ForeignKey("flights.id"),nullable = False)
  