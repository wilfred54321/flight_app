from flask import Blueprint
from flight_app.models import db,Schedule
from flask import redirect,flash,request


schedule = Blueprint('schedule', __name__)

@schedule.route('/flight/schedule/<int:schedule_id>/delete', methods = ['GET'])
def cancel_schedule(schedule_id):
    #retrive the schedule for the database
    schedule = Schedule.query.get(schedule_id)

    #check the status of the schedule to be sure it is available
    #a schedule is available if the plane is not currently in the air. 
    
    db.session.delete(schedule)
    db.session.commit()
    message = f"Flight scheduled for {schedule.origin} to {schedule.destination} has been cancelled"
    flash(message,'info')
    return redirect(request.referrer)