# import logging
from logging import DEBUG
import os
from pathlib import Path
import csv
from flask import Flask, render_template, request, flash
from models import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("FLIGHTAPP_DB_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "dfe56e985611aa6f"
db.init_app(app)

# logging.basicConfig(filename="logfile.log", level=logging.DEBUG)


@app.route("/")
def index():
    """Diplay a list of Flights"""

    flights = Flight.query.all()
    return render_template("index.html", flights=flights)


@app.route("/book-flight")
def book_flight():
    """Diplay a list of Flights"""

    flights = Flight.query.all()
    return render_template("book.html", flights=flights)


@app.route("/flights/<int:flight_id>")
def flight(flight_id):

    try:
        flight = Flight.query.get_or_404(flight_id)
    except ValueError:
        return render_template("error.html", message="No such flight is available")

    # passengers = flight.passengers
    # open_seats = flight.open_seats()
    # pilot = flight.pilots

    return render_template("flight.html", flight=flight)


@app.route("/book", methods=["GET", "POST"])
def book():
    """Book a flight"""
    if request.method != "POST":

        flights = Flight.query.all()
        render_template("book.html", flights=flights)
    else:

        firstname = (request.form.get("firstname")).capitalize()
        lastname = (request.form.get("lastname")).capitalize()
        gender = request.form.get("gender")

        # try:
        #     flight_id = int(request.form.get("flight_id"))
        # except ValueError:
        #     return render_template("error.html", message ="Invalid flight id")
        flight_origin = request.form.get("flight_origin")
        flight_destination = request.form.get("flight_destination")
        try:
            flight = Flight.query.filter_by(
                origin=flight_origin, destination=flight_destination
            ).first()
        except:
            return render_template("error.html", message="Flight is invalid")

        # Make sure the flight exists
        # flight = Flight.query.get(flight_id)
        if flight is None:
            return render_template(
                "error.html",
                message="Ooops!. It appears there is no flight for the routes you selected.",
            )

        # Add Passenger if there are open seats and the flight is not null

        if flight.open_seats():

            flight.add_passenger(firstname, lastname, gender, flight.id)

            return render_template(
                "success.html", message="You have successfully booked your flight"
            )

        else:
            return render_template(
                "error.html", message="No more seats available on this flight"
            )


@app.route("/manage-booking   ", methods=["GET", "POST"])
def manage_booking():
    """Manage an already booked flight"""
    if request.method == "POST":
        lastname = (request.form.get("lastname")).capitalize()
        booking_reference = (request.form.get("booking_reference")).upper()

        # check if the record exists in the database
        passenger = Passenger.query.filter_by(
            lastname=lastname, booking_reference=booking_reference
        ).first()
        if passenger:
            return render_template("book.html", passenger=passenger)
        else:
            message = f"No passenger exists with lastname: {lastname} and booking reference: {booking_reference}"
            flash(message, "danger")
    return render_template("book.html")


@app.route("/upload-flight", methods=["GET", "POST"])
def upload_flight():

    if request.method == "POST":
        filename = request.form.get("file_name")
        dir = "./static/flight_data/"
        flight_csv_data = dir + filename

        with open(flight_csv_data) as file:
            flight_data = csv.reader(file)
            for (
                code,
                origin,
                destination,
                capacity,
                departure_time,
                arrival_time,
            ) in flight_data:
                flight = Flight(
                    code=code,
                    origin=origin,
                    destination=destination,
                    capacity=capacity,
                    departure_time=departure_time,
                    arrival_time=arrival_time,
                )
                db.session.add(flight)
        db.session.commit()
        # return f"<h1>flight {code} from {origin} to {destination} added successfully!</h1>"

        return render_template("index.html")

    # if request.method == "POST":
    #     # get the flight origin,destination and code
    #     flight_origin = request.form.get("flight_origin")
    #     flight_destination = request.form.get("flight_destination")
    #     flight_code = request.form.get("flight_code").upper()
    #     delay_amount = int(request.form.get("delay_amount"))
    #     return f"<h1>{delay_amount}</h1>"
    # Query the database for the given flight
    # flight = Flight.query.filter_by(
    #     origin=flight_origin,
    #     destination=flight_destination,
    #     code=flight_code,
    # ).first()
    # if not flight:
    #     message = "No such flight exist. Please, ensure you enter the correct flight origin,destination and flight code!"
    #     return render_template("error.html", message=message)
    # else:
    #     # delay light by delay amount
    #     flight.delay_flight(delay_amount)
    #     # db.session.add(flight)
    #     # db.session.commit()
    #     return f"<h1>Return value: {flight.delay_flight(delay_amount)},Flight Duration: {((flight.arrival_time - flight.departure_time).total_seconds())//60}</h1>"

    # else:
    #     return "<p>GET method is not acceptable. please use the post method to post your data!</p>"


@app.route("/flight/delay", methods=["GET", "POST"])
def delay_flight():
    if request.method == "POST":
        return "<h1>Hello!</h1>"
    else:
        return "<h1>Request method is GET</h1>"


if __name__ == "__main__":
    app.run(debug=1)
