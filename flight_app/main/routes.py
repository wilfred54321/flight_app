from flask import Blueprint


from logging import DEBUG
import os
from pathlib import Path
from sqlalchemy import desc
import csv
from flask import Flask, render_template, request, flash, redirect, url_for
from flight_app.models import Flight, Passenger, db, datetime, Pilot
from flight_app.utils import is_valid_flight_time
from flight_app.models import add_flight

main = Blueprint("main", __name__)


# logging.basicConfig(filename="logfile.log", level=logging.DEBUG)
# HELPER FUNCTIONS


@main.route("/")
def index():
    """Display a list of Flights and Pilots"""
    pilots = Pilot.query.order_by(desc(Pilot.firstname)).limit(3).all()
    flights = Flight.query.all()
    return render_template("index.html", pilots=pilots, flights=flights, title="Index")


@main.route("/book-flight")
def book_flight():
    """Diplay a list of Flights"""

    flights = Flight.query.all()
    return render_template("book.html", flights=flights, title="Booking")


@main.route("/flights/<int:flight_id>")
def flight(flight_id):
    try:
        flight = Flight.query.get_or_404(flight_id)
    except ValueError:
        return render_template("error.html", message="No such flight is available")
    return render_template("flight.html", flight=flight)


@main.route("/book", methods=["GET", "POST"])
def book():
    """Book a flight"""
    if request.method != "POST":
        flights = Flight.query.all()
        render_template("book.html", flights=flights)
    else:
        firstname = (request.form.get("firstname")).capitalize()
        lastname = (request.form.get("lastname")).capitalize()
        gender = request.form.get("gender")
        flight_origin = request.form.get("flight_origin")
        flight_destination = request.form.get("flight_destination")
        try:
            flight = Flight.query.filter_by(
                origin=flight_origin, destination=flight_destination
            ).first()
        except:
            return render_template("error.html", message="Flight is invalid")
        # Make sure the flight exists
        if flight is None:
            return render_template(
                "error.html",
                message="Ooops!. It appears there is no flight for the routes you selected.",
            )
        # Add Passenger if there are open seats and the flight is not null
        if flight.open_seats():
            booking_reference = flight.add_passenger(
                firstname, lastname, gender, flight.id
            )
            return render_template(
                "success.html",
                message=f"You have successfully booked your flight. Your reference id is {booking_reference}",
            )
        else:
            return render_template(
                "error.html", message="No more seats available on this flight"
            )


@main.route("/manage-booking   ", methods=["GET", "POST"])
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


@main.route("/flight/delay", methods=["GET", "POST"])
def delay_flight():
    if request.method == "POST":
        # get the flight origin,destination and code
        flight_origin = request.form.get("flight_origin")
        flight_destination = request.form.get("flight_destination")
        flight_code = request.form.get("flight_code").upper()
        delay_amount = int(request.form.get("delay_amount"))
        # return f"<h1>{(flight_code)}</h1>"
        # Query the database for the given flight
        flight = Flight.query.filter_by(
            origin=flight_origin,
            destination=flight_destination,
            code=flight_code,
        ).first()
        if not flight:
            message = "No such flight exist. Please, ensure you enter the correct flight origin,destination and flight code!"
            return render_template("error.html", message=message)
        else:
            # delay light by delay amount
            new_arrival_time = flight.delay_flight(delay_amount)
            flight.arrival_time = new_arrival_time
            db.session.commit()
            message = "Flight {} from {} to {} has been delayed by {}minutes. New Arrival Time is {}".format(
                flight.code,
                flight.origin,
                flight.destination,
                delay_amount,
                flight.arrival_time,
            )
            return render_template("success.html", message=message)
            # return f"<h1>Original arival time:{flight.arrival_time},\n New Arrival Time: {flight.delay_flight(delay_amount)}\n Flight Duration: {((flight.arrival_time - flight.departure_time).total_seconds())//60}</h1>"

    else:
        return render_template("book-flight.html")


@main.route("/flight/<int:flight_id>/delete", methods=["GET"])
def delete_flight(flight_id):

    flight = Flight.query.get_or_404(flight_id)
    if flight:
        db.session.delete(flight)
        db.session.commit()
        message = f"Flight {flight.code} deleted successfully!"
        flash(message, "success")
        return redirect(url_for("main.index"))
    return render_template("error.html", message="Flight does not exist")


@main.route("/flight/<int:flight_id>/edit", methods=["GET", "POST"])
def edit_flight(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    return render_template("index.html", flight=flight)


@main.route("/passenger/<int:flight_id>/<int:passenger_id>", methods=["GET"])
def delete_passenger(passenger_id, flight_id):
    flight = Flight.query.get_or_404(flight_id)
    passenger = Passenger.query.get(passenger_id)
    db.session.delete(passenger)
    db.session.commit()
    message = f"""Passenger \'{passenger.firstname} {passenger.lastname}\' was successfully deleted from 
    flight {flight.code} from {flight.origin} to {flight.destination}"""
    flash(message, "success")
    return redirect(url_for("main.flight", flight_id=flight_id))
