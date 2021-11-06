from flask import Blueprint
from flask import render_template, redirect, request, flash, url_for


from flight_app.models import db, Pilot,Passenger,Schedule
users = Blueprint("users", __name__)


@users.route("/all-pilots", methods=["POST", "GET"])
def all_pilots():
    # pilots = Pilot.query.all()
    # # return pilots
    # return render_template("index.html", pilots=pilots, title="Index")
    pass


@users.route("/register-pilot", methods=["GET", "POST"])
def register_pilot():
    if request.method == "POST":
        firstname = request.form.get("firstname").capitalize()
        lastname = request.form.get("lastname").capitalize()
        email = request.form.get("email").lower()
        gender = request.form.get("gender")
        cat = request.form.getlist("category")
        category = [x for x in cat]

        level = request.form.get("pilot_level")

        pilot = Pilot(
            firstname=firstname,
            lastname=lastname,
            email=email,
            gender=gender,
            category=category,
            level=level,
        )
        db.session.add(pilot)
        db.session.commit()

        flash(f"Pilot {firstname}, {lastname} was registered successfully!", "success")
        return redirect(url_for("main.index"))

    return render_template("index.html", title="Index")


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
    passengers = Passenger.query.filter_by(id = schedule_id)
    flight_schedule = Schedule.query.get(schedule_id)
    return render_template('passengers.html',passengers = passengers,flight = flight_schedule)