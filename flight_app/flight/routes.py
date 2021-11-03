from flask import Blueprint, render_template
from flight_app.models import Flight

flight = Blueprint("flight", __name__)


@flight.route("/flight/<int:flight_id>/add-passenger", methods=["GET", "POST"])
def add_passenger(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    return render_template("book.html", flight=flight)
