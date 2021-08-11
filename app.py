import os
import csv
from flask import Flask, render_template,request
from models import *
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("FLIGHTAPP_DB_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
db.init_app(app)



@app.route("/")
def index():
    """Diplay a list of Flights"""

    flights = Flight.query.all()
    return render_template("index.html",flights=flights)



@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    try:
        flight = Flight.query.get(flight_id)
    except ValueError:
        return render_template("error.html", message = "No such flight is available")

    passengers = flight.passengers
    pilot = flight.pilots

    return render_template ("flight.html",flight = flight, passengers = passengers,pilot = pilot)

    

@app.route("/book", methods = ["GET","POST"])
def book():
    """Book a flight"""
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    gender = request.form.get("gender")

    try:
        flight_id = int(request.form.get("flight_id")) 
    except ValueError: 
        return render_template("error.html", message ="Invalid flight id")
    
    #Make sure the flight exists
    flight = Flight.query.get(flight_id)

    if flight is None:
        return render_template("error.html", message = "flight does not exist")
    
    #Add Passenger if the flight is not null
    # passenger = Passenger(firstname,lastname,gender,flight_id)
    # db.session.add(passenger)
    # db.session.commit()
    flight.add_passenger(firstname,lastname,gender)
    return render_template("success.html", message = "You have successfully booked your flight")
   
 

    
