from flask import Blueprint
from flask import render_template, redirect, request, flash, url_for

import flight_app
from flight_app.models import db, Pilot, Passenger, Flight

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
        category = request.form.getlist("category")
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

        # context = {
        #     "firstname": firstname,
        #     "lastname": lastname,
        #     "email": email,
        #     "gender": gender,
        #     "category": category,
        #     "level": level,
        # }

        # return f"<h1>Firstname is {context['firstname']}</h1>"
        # return render_template("test.html", **context)
    return render_template("index.html", title="Index")
