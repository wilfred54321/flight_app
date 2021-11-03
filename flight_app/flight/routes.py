from flask import Blueprint, render_template, request, redirect, url_for
import csv
from flight_app.models import Flight
from flight_app.models import db, add_flight
from flight_app.utils import is_valid_flight_time, datetime

flight = Blueprint("flight", __name__)


@flight.route("/flight/<int:flight_id>/add-passenger", methods=["GET", "POST"])
def add_passenger(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    return render_template("book.html", flight=flight)


@flight.route("/upload-flight", methods=["GET", "POST"])
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
                flight = add_flight(
                    code, origin, destination, capacity, departure_time, arrival_time
                )
                db.session.add(flight)
        db.session.commit()
        # return f"<h1>flight {code} from {origin} to {destination} added successfully!</h1>"
        return render_template("index.html")


@flight.route("/schedule_flight", methods=["GET", "POST"])
def schedule_flight():

    if request.method == "POST":
        flight_code = request.form.get("flight_code").upper()
        flight_origin = (request.form.get("flight_origin")).capitalize()
        flight_destination = (request.form.get("flight_destination")).capitalize()
        flight_departure_time = request.form.get("departure_time")
        flight_arrival_time = request.form.get("arrival_time")
        flight_capacity = request.form.get("flight_capacity")

        departure_time = format_datetime(flight_departure_time)
        arrival_time = format_datetime(flight_arrival_time)

        if is_valid_flight_time(departure_time, arrival_time):

            flight = add_flight(
                flight_code,
                flight_origin,
                flight_destination,
                flight_capacity,
                flight_departure_time,
                flight_arrival_time,
            )

            db.session.add(flight)
            db.session.commit()

            message = f"""flight_code: {flight_code} from {flight_origin} to {flight_destination}\n
            departure time: {departure_time},\n arrival time: {arrival_time},\nflight capacity: {flight_capacity} was
            added successfully!"""

            # logging.DEBUG(message)
            return render_template("success.html", message=message)

        return render_template(
            "error.html",
            message="Please ensure the arrival time is valid and departure time is at least two hours from the current time!",
        )

        # dl = departure_time.split("T")
        # dt = "".join(map(str, dl))
        # new_date = datetime.strptime(dt, "%Y-%m-%d%H:%M")
        # print(dt)
        # new_date = departure_time.strftime('%B %d, %Y')

        # new_date = format_datetime(departure_time)
        # return f"<h1>{new_date}</h1>"

    return render_template("schedule_flight.html")


# function to format datetime for writing to database
def format_datetime(form_input):
    datetime_data = form_input.split("T")
    str_datetime_data = "".join(map(str, datetime_data))
    return datetime.strptime(str_datetime_data, "%Y-%m-%d%H:%M")
