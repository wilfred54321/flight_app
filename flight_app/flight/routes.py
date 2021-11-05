from flask import Blueprint, render_template, request, redirect, url_for, flash
import csv



from flight_app.models import db,Flight

from flight_app.utils import format_datetime,is_invalid_date_of_first_flight, is_valid_flight_time

flight = Blueprint("flight", __name__)


@flight.route("/flight/<int:flight_id>/add-passenger", methods=["GET", "POST"])
def add_passenger(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    return render_template("book.html", flight=flight)


@flight.route("/upload-flight", methods=["GET", "POST"])
def upload_flight():
    pass


#     if request.method == "POST":
#         filename = request.form.get("file_name")
#         dir = "./static/flight_data/"
#         flight_csv_data = dir + filename

#         with open(flight_csv_data) as file:
#             flight_data = csv.reader(file)
#             for (
#                 code,
#                 origin,
#                 destination,
#                 capacity,
#                 departure_time,
#                 arrival_time,
#             ) in flight_data:
#                 flight = add_flight(
#                     code, origin, destination, capacity, departure_time, arrival_time
#                 )
#                 db.session.add(flight)
#         db.session.commit()

#         return render_template("index.html")


import os


@flight.route("/register-new-flight", methods=["GET", "POST"])
def register_new_flight():
    if request.method == "POST":
        flight_code = request.form.get("flight_code").upper()
        flight_capacity = request.form.get("flight_capacity")
        flight_model = request.form.get("flight_model")
        category = request.form.get("flight_category")
        date_of_first_flight = format_datetime(request.form.get("first_flight_date"))

        # check to ensure that the flight does not already exist in the database
        flight = Flight.query.filter_by(code=flight_code).first()
        if flight:
            message = "Sorry, A flight with thesame code already exist."
            flash(message, "danger")
            return render_template('register_new_flight.html')

        # Add flight to database
        if is_invalid_date_of_first_flight(date_of_first_flight):
            message = "Sorry, The date of first flight must not be in the future."
            flash(message, "danger")
            return render_template('register_new_flight.html')
        flight = Flight(
        code=flight_code,
        capacity=flight_capacity,
        model=flight_model,
        category=category,
        date_of_first_flight=date_of_first_flight)
        db.session.add(flight)
        db.session.commit()
        
        message = f"Flight {flight_code} with a capacity of {flight_capacity} was added successfully!"
        flash(message, "success")
        return render_template('main.index.html')
    return render_template("register_new_flight.html", title="Register Flight")



@flight.route("/flight/status/<int:flight_id>/<string:action>", methods=["GET", "POST"])
def change_status(flight_id, action):
    flight = Flight.query.get(flight_id)
    # get pilot

    if action == "enable":
        flight.enable()
        flash(f'Flight {flight.code} has been enabled. You can now schedule it for a route','success')
        return redirect(request.referrer)
    flight.disable()
    flash(f'Flight {flight.code} has been disabled','info')
    return redirect(request.referrer)


@flight.route("/schedule_flight/<int:flight_id>", methods=["GET", "POST"])
def schedule_flight(flight_id):
    
    """This function schedules an already registered flight by assigning it an origin, destination,
    capacity,departure datetime, arrival datetime. Once the flight is schedule, passengers are able to
    book the flight. It becomes unaviable for schedule once it is scheduled."""

    #check if the flight is available
    flight = Flight.query.get_or_404(flight_id)
    if flight.is_available == False:
        flash('Sorry, This flight is currently unavailable and cannot be scheduled!','danger')
        return redirect(request.referrer)
    return render_template('schedule_flight.html',flight = flight, title = 'Schedule Flight')









@flight.route("/process_flight/<int:flight_id>", methods=["GET", "POST"])
def process_flight_schedule(flight_id):
    """Process the received form"""

    if request.method == "POST":
        # flight_code = request.form.get("flight_code").upper()
        flight_origin = (request.form.get("flight_origin")).capitalize()
        flight_destination = (request.form.get("flight_destination")).capitalize()
        flight_departure_time = request.form.get("departure_time")
        flight_arrival_time = request.form.get("arrival_time")
        # flight_capacity = request.form.get("flight_capacity")

        #FORMAT FLIGHT DEPARTURE AND ARRIVAL TIME TO DB COMPATIBLE
        departure_time = format_datetime(flight_departure_time)
        arrival_time = format_datetime(flight_arrival_time)

        if not is_valid_flight_time(departure_time, arrival_time):
            flash('Please ensure the flight time is valid. It must be at least two hours from the current time.')
            return "flight time not valid"
            # return redirect(request.referrer)
        flight = Flight.query.get_or_404(flight_id)


        flight.schedule_flight(flight_origin,flight_destination,flight_departure_time,flight_arrival_time)

        message = f"""flight_code: {code} from {flight_origin} to {flight_destination}\n
        departure time: {departure_time},\n arrival time: {arrival_time},\nflight capacity: {flight_capacity} was
        added successfully!"""
        flash(message,'success')
        return redirect(url_for('main.index'))
        return render_template("schedule_flight.html")





