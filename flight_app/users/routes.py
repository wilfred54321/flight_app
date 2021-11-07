from flask import Blueprint
from flask import render_template, redirect, request, flash, url_for


from flight_app.models import db, Pilot,Passenger,Schedule,scheduled_pilots
users = Blueprint("users", __name__)


@users.route("/all-pilots", methods=["POST", "GET"])
def all_pilots():
    pilots = Pilot.query.all()
    # return f"{pilots}"
    return render_template("index.html", pilots=pilots, title="Index")

@users.route("/all-passenger",methods = ['POST','GET'])
def all_passengers():

    passengers_name = []
    passengers = Passenger.query.all()
    for passenger in passengers:
        passengers_name.append(passenger.firstname)
    return f"{passengers_name}"


@users.route("/register-pilot", methods=["GET", "POST"])
def register_pilot():
    if request.method == "POST":
        firstname = request.form.get("firstname").capitalize()
        lastname = request.form.get("lastname").capitalize()
        email = request.form.get("email").lower()
        gender = request.form.get("gender")
        # cat = request.form.getlist("category")
        # category = [x for x in cat]
        level = request.form.get("pilot_level")

        pilot = Pilot(
            firstname=firstname,
            lastname=lastname,
            email=email,
            gender=gender, 
            level=level,
        )
        db.session.add(pilot)
        db.session.commit()

        flash(f"Pilot {firstname}, {lastname} was registered successfully!", "success")
        # print(type(gender))
        # flash(f'{gender}','danger')
        return redirect(url_for("main.index"))

    return render_template("create_pilot.html", title="Index")


@users.route("/schedule_pilot", methods=["GET", "POST"])
def schedule_pilot():
    return render_template("create_pilot.html")


@users.route("/pilot/status/<int:pilot_id>/<string:action>", methods=["GET", "POST"])
def change_status(pilot_id, action):
    pilot = Pilot.query.get(pilot_id)
    # get pilot

    if action == "enable":
        pilot.enable()
        return redirect(request.referrer)
    pilot.disable()
    return redirect(request.referrer)


@users.route("/delete-pilot/<int:pilot_id>)", methods=["GET"])
def delete_pilot(pilot_id):
    pilot = Pilot.query.get_or_404(pilot_id)
    if pilot.is_available:
        message = "Sorry, You must first disable pilot before you can delete!"
        flash(message, "info")
        return redirect(request.referrer)
    db.session.delete(pilot)
    db.session.commit()
    flash(f"Pilot {pilot.firstname}, {pilot.lastname} deleted successfully!", "success")
    return redirect(request.referrer)


@users.route('/flight/schedule/passenger/<int:schedule_id>', methods = ['GET'])
def show_passengers(schedule_id):
    # passengers = Passenger.query.filter_by(id = schedule_id).all()
    flight_schedule = Schedule.query.get(schedule_id)
    pilots = Pilot.query.join(scheduled_pilots).join(Schedule).filter((scheduled_pilots.c.pilot_id == Pilot.id) &(scheduled_pilots.c.schedule_id==schedule_id)).all()
    return render_template('passengers.html',schedule = flight_schedule,pilots = pilots)


@users.route("/show-all-pilots",methods = ['POST','GET'])
def show_all_pilots():
    pilots = Pilot.query.all()
    return render_template('pilots.html', pilots = pilots)

# @users.route("/show/<int:schedule_id>",methods = ['POST','GET'])
# def show_scheduled_pilots(schedule_id):
#     p_names = []
#     pilots = Pilot.query.join(scheduled_pilots).join(Schedule).filter((scheduled_pilots.c.pilot_id == Pilot.id) &(scheduled_pilots.c.schedule_id==schedule_id)).all()
    
#     for pilot in pilots:
#         p_names.append(pilot.firstname)
#     return f"{p_names}"

      

@users.route("/passenger/check-in/<int:passenger_id>", methods = ['GET','POST'])
def passenger_check_in(passenger_id):
    passenger = Passenger.query.get(passenger_id)
    if passenger.status() == 'checked in':
       flash('You are already checked in','info')
       return redirect(url_for('main.manage_booking'))
    passenger.is_checked_in = True
    db.session.commit()
    flash('You are now checked in','success')
    return redirect(url_for('main.manage_booking'))
    
    