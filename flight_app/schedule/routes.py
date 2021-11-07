from flask import Blueprint
from flight_app.models import db,Schedule,Pilot
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


@schedule.route('/schedule/delete', methods = ['POST','GET'])
def checkbox_cancel_schedule():
   input = request.form.getlist('checkbox')
   if input == None:

        input = request.form.getlist('all')
   result = [int(x) for x in input]
   schedule_reference = []
   for schedule_id in result:
       schedule = Schedule.query.get(schedule_id)
       schedule_reference.append(schedule.id)
       db.session.delete(schedule)
   db.session.commit()
   message = f"Schedules with ID {schedule_reference} were deleted successfully!"
   flash(message,'success')
   return redirect(request.referrer)

@schedule.route("/flight/schedule/assign-pilot<int:schedule_id>", methods = ['GET','POST'])
def assign_pilot(schedule_id):
    schedule_id = schedule_id
    schedule = Schedule.query.get(schedule_id)
    print(schedule.schedules)
    # if schedule.schedules is None:
    return "No Pilot has been assigned to this flight!"
    # return "This flight has at least one pilot assigned already!"

    # print(schedule_id)
    # schedule = Schedule.query.get(schedule_id)
    # pilot = Pilot.query.get(1)
    # schedule.schedules.append(pilot)
    # db.session.commit()
    # flash(f'Pilot {pilot.firstname}, {pilot.lastname} has been assigned to Flight scheduled for {schedule.origin} to {schedule.destination}','success')
    # return redirect(request.referrer)

