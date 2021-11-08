from flask import Blueprint, render_template, request, redirect, url_for, flash
import csv



from flight_app.models import db,Flight,Schedule

from flight_app.utils import format_datetime,is_invalid_date_of_first_flight, is_valid_flight_time,timedelta

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
        return render_template('index.html')
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
        
        flight_origin = (request.form.get("flight_origin")).capitalize()
        flight_destination = (request.form.get("flight_destination")).capitalize()
        flight_departure_time = request.form.get("departure_time")
        flight_arrival_time = request.form.get("arrival_time")
        flight_capacity = int(request.form.get('flight_capacity'))
       

        #FORMAT FLIGHT DEPARTURE AND ARRIVAL TIME TO DB COMPATIBLE
        departure_time = format_datetime(flight_departure_time)
        arrival_time = format_datetime(flight_arrival_time)

        if not is_valid_flight_time(departure_time, arrival_time):
            flash('Please ensure the flight time is valid. It must be at least two hours from the current time.','danger')
            return redirect(request.referrer)
            # return redirect(request.referrer)
        flight = Flight.query.get_or_404(flight_id)


        schedule = flight.schedule_flight(flight_origin,flight_destination,flight_capacity,departure_time,arrival_time)


        # message = f"""flight_code: {code} from {flight_origin} to {flight_destination}\n
        # departure time: {departure_time},\n arrival time: {arrival_time},\nflight capacity: {flight_capacity} was
        # added successfully!"""
        message = f"Flight {schedule.flight.code} from {schedule.origin} to {schedule.destination} scheduled successfully!"
        flash(message,'success')
        return redirect(url_for('main.flight',flight_id = flight_id))
        # return render_template("schedule_flight.html")





@flight.route("/flight/delay/<int:schedule_id>", methods=["GET", "POST"])
def delay_flight(schedule_id):

    if request.method =="POST":
        #retrieve the delay amount from the form
        delay_amount = int(request.form.get('delay_amount'))
        #query the database with the schedule amount to get the schedule object
        
       
        schedule = Schedule.query.get_or_404(schedule_id)
        schedule.delay_flight(delay_amount)
        message = f"""Flight from {schedule.origin} to {schedule.destination} 
        has been delay for {delay_amount} mins. The new arrival time is {schedule.arrival_time}"""
        flash(message,'success')
        return redirect(url_for('main.flight',flight_id = schedule.flight.id))
    return render_template('delay_flight.html',schedule_id = schedule_id)



        # get the flight origin,destination and code
        # flight_origin = request.form.get("flight_origin")
        # flight_destination = request.form.get("flight_destination")
        # flight_code = request.form.get("flight_code").upper()
        # delay_amount = int(request.form.get("delay_amount"))
        # # return f"<h1>{(flight_code)}</h1>"
        # # Query the database for the given flight
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
        #     new_arrival_time = flight.delay_flight(delay_amount)
        #     flight.arrival_time = new_arrival_time
        #     db.session.commit()
        #     message = "Flight {} from {} to {} has been delayed by {}minutes. New Arrival Time is {}".format(
        #         flight.code,
        #         flight.origin,
        #         flight.destination,
        #         delay_amount,
        #         flight.arrival_time,
        #     )
        #     return render_template("success.html", message=message)
            # return f"<h1>Original arival time:{flight.arrival_time},\n New Arrival Time: {flight.delay_flight(delay_amount)}\n Flight Duration: {((flight.arrival_time - flight.departure_time).total_seconds())//60}</h1>"

    # else:
    #     return render_template("book-flight.html")

@flight.route("/flight/<int:flight_id>/delete", methods=["GET"])
def delete_flight(flight_id):

    flight = Flight.query.get_or_404(flight_id)
    if flight:
        #check if flight is disabled before deleting
        if flight.is_available == True:
            flash('sorry, you must first disable flight before you can delete','danger')
            return redirect(request.referrer)
        db.session.delete(flight)
        db.session.commit()
        message = f"Flight {flight.code} deleted successfully!"
        flash(message, "success")
        return redirect(request.referrer)
    flash('Error: Flight does not exist','danger')
    return render_template('index.html')


@flight.route("/flight/<int:flight_id>/edit", methods=["GET", "POST"])
def edit_flight(flight_id):
    if request.form == 'POST':

        #GET THE FORM REQUESTS
        flight_code = request.form.get("flight_code").upper()
        flight_capacity = request.form.get("flight_capacity")
        flight_model = request.form.get("flight_model")
        category = request.form.get("flight_category")
        date_of_first_flight = format_datetime(request.form.get("first_flight_date"))


        # #QUERY THE DB AND REASSIGN THE VALUES IN THE DATABASE
        # flight = Flight.query.get_or_404(flight_id)

        # if not flight:
        #     flash('sorry, flight is invalid')
        #     return redirect(request.referrer)
        # else
        #     code = flight_code,
        #     c
        
        # fligh
        # #COMMIT THE CHANGES

        #EDIT FUNCTION
        print("Request is a post request.")
        flight = Flight.query.get_or_404(flight_id)
        return f"This will process the edit function for flight {flight.code}"
    flight = Flight.query.get_or_404(flight_id)
    return render_template('register_new_flight.html',flight = flight)


    
@flight.route("/test", methods = ['GET','POST'])
def flight_test():
    input = request.form.getlist('checkbox')
    return f"<h1>{input}</h1>"