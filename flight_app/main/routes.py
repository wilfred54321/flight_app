from flask import Blueprint


from logging import DEBUG
import os
from pathlib import Path
from sqlalchemy import desc
import csv
from flask import Flask, render_template, request, flash, redirect, url_for
from flight_app.models import Flight,Pilot,Passenger,db,Schedule



main = Blueprint("main", __name__)



@main.route("/")
def index():
    """Display a list of Flights and Pilots"""
    pilots = Pilot.query.order_by(desc(Pilot.firstname)).all()
    flights = Flight.query.all()
    if flights == None and pilots == None:
        return render_template('index.html', title = 'Index')
    return render_template("index.html", pilots=pilots, flights=flights, title="Index")








@main.route("/book-flight", methods = ['GET','POST'])
def book_flight():
    """Diplay a list of Flights"""
    if request.method == 'POST':
        firstname = (request.form.get("firstname")).capitalize()
        lastname = (request.form.get("lastname")).capitalize()
        gender = request.form.get("gender")
        flight_origin = request.form.get("flight_origin")
        flight_destination = request.form.get("flight_destination")
        email = request.form.get('email')
        try:
            schedule = Schedule.query.filter_by(
                origin=flight_origin, destination=flight_destination
            ).first()
        except:
            return render_template("error.html", message="Flight is invalid")
        # Make sure the flight exists
        if schedule is None:
            message="Ooops!. It appears there is no flight scheduled for the routes you selected."
            flash(message,'danger')
            return redirect(request.referrer)
        # Add Passenger if there are open seats and the flight is not null
        if schedule.open_seats():
            booking_reference = schedule.add_passenger(
                firstname, lastname, gender,email
            )             
            message=f"You have successfully booked your flight. Your reference id is {booking_reference}"
            flash(message,'success')
            return redirect(url_for('main.index'))
            
        
        message="No more seats available on this flight"
        flash(message,'info')
        return redirect(request.referrer)
    
    
    flights_schedule = Schedule.query.all()
    return render_template("book.html", flights=flights_schedule, title="Booking")
    


@main.route("/book/<int:schedule_id>", methods = ["GET", "POST"])
def book(schedule_id):
    """Book a flight"""
    if request.method != "POST":
        schedule = Schedule.query.get(schedule_id)
        if schedule.open_seats():
        #Make an API call to populate form with some flight origin and destinations
            return render_template("book.html", flight=schedule)
        message = "No more available seats"
        flash(message,'info')
        return redirect(request.referrer)
    return redirect('main.book_flight')
   











@main.route("/flights/<int:flight_id>")
def flight(flight_id):
    try:
        flight = Flight.query.get_or_404(flight_id)
        
    except ValueError:
        return render_template("error.html", message="No such flight is available")
    return render_template("flight.html", flight=flight)






#         

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
