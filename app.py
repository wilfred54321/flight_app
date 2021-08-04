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
    # greetings = "Hello World"
    # return render_template("index.html",greetings=greetings)

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

    return render_template ("flight_info.html",flight = flight, passengers = passengers, pilot = pilot)

    

