from flask import Blueprint
from flight_app.models import db,Schedule,Pilot
from flask import redirect,flash,request,session,url_for


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
        if input == []:
            flash('Please select a flight schedule to cancel','info')
            return redirect(request.referrer)

    
    # flash('Please select a flight schedule to cancel','info')
    # return redirect(request.referrer)
   else:
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





@schedule.route("/flight/schedule/assign-pilot/<int:schedule_id>", methods = ['GET','POST'])
def assign_schedule(schedule_id):
    
    # return f"schedule id is {schedule_id}"
    #get the flight id from the schedule url
    #save it in a section and redirect to the all pilots page to retrieve the pilot id
        session['schedule_id'] = schedule_id

        return redirect(url_for('users.all_pilots')) 
        
     #post it to the assign_pilot form
    #query the association table and bind the schedule id to a user id
@schedule.route("/flight/schedule/assign-pilot", methods = ['POST','GET'])
def assign_pilot():
    if request.method == 'POST':
        pilot_id = request.form.get('checkbox')
        schedule_id = session.get('schedule_id')

         #Query the schedule and session tables
        schedule = Schedule.query.get(schedule_id)
        pilot = Pilot.query.get(pilot_id)
        
        if pilot.is_available == True:
            schedule.schedules.append(pilot)
            db.session.commit()
            session.clear()
            #Email Pilot notifying him of his schedule!
            flash(f"Pilot {pilot.firstname}, {pilot.lastname} has been assigned to Flight {schedule.flight.code} scheduled for {schedule.origin} to {schedule.destination}",'success')
            return redirect(url_for('users.show_passengers',schedule_id = schedule_id))
        
        flash(f"Could not assign pilot {pilot.firstname}, {pilot.lastname} to flight {schedule.flight.code}. Please ensure the Pilot is available.",'danger')
        return redirect(url_for('users.all_pilots'))

#   return f"Schedule_id is : {schedule_id}, Pilot_id is : {pilot_id}"
#     schedule = Schedule.query.get(schedule_id)
#     print(schedule.schedules)

# @schedule.route("/flight/schedule/assign-pilot", methods = ['POST','GET'])
# def assign_pilot():
#     if request.method == 'POST':
#         pilot_id = request.form.get('checkbox')
        
#         return f" Pilot_id is : {pilot_id}"
    # return "Method not allowed."
    # if schedule.schedules is None:
    # return "No Pilot has been assigned to this flight!"
    # return "This flight has at least one pilot assigned already!"

    # print(schedule_id)
    # schedule = Schedule.query.get(schedule_id)
    # pilot = Pilot.query.get(1)
    # schedule.schedules.append(pilot)
    # db.session.commit()
    # flash(f'Pilot {pilot.firstname}, {pilot.lastname} has been assigned to Flight scheduled for {schedule.origin} to {schedule.destination}','success')
    # return redirect(request.referrer)

