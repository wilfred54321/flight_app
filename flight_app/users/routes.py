from flask import Blueprint
from flask import render_template, redirect, request, flash, url_for,session
from flask_login.utils import login_required, logout_user
from flight_app.users.forms import LoginForm, RegistrationForm, SetPasswordForm
from flask_login import login_user,current_user
from flight_app import bcrypt, logging


from flight_app.models import db, Pilot, Flight, Passenger, Schedule, scheduled_pilots
from flight_app.users.models import User,admin_required

users = Blueprint("users", __name__)


@users.route("/all-pilots", methods=["POST", "GET"])
def all_pilots():
    pilots = Pilot.query.all()
    flights = Flight.query.all()
    # return f"{pilots}"
    return render_template("index.html", flights=flights, pilots=pilots, title="Index")


@users.route("/all-passenger", methods=['POST', 'GET'])
def all_passengers():
    passengers = Passenger.query.order_by(Passenger.timestamp.desc())
    return render_template('all_passengers.html', passengers=passengers)


@users.route("/register-pilot", methods=["GET", "POST"])
@login_required
@admin_required
def register_pilot():
    if request.method == "POST":
        try:

            firstname = request.form.get("firstname").capitalize()
            lastname = request.form.get("lastname").capitalize()
            email = request.form.get("email").lower()
            gender = request.form.get("gender")
            category = request.form.get("category")
            level = request.form.get("pilot_level")

            # Query the database to be sure the email does not exist

            pilot = Pilot.query.filter_by(email=email).first()
            if pilot:
                flash('Sorry, a pilot with this email address already exist. Please choose another email address!',
                      'danger')
                return redirect(request.referrer)

            pilot = Pilot(
                firstname=firstname,
                lastname=lastname,
                email=email,
                gender=gender,
                category=category,
                level=level,
                is_available=False
            )
            db.session.add(pilot)
            db.session.commit()
            message = f"Pilot {firstname}, {lastname} with ID {pilot.pilot_id}\
             was registered successfully by user ({current_user.firstname},{current_user.lastname}) "
            flash(message,"success")
            logging.DEBUG(message)
            # print(type(gender))
            # flash(f'{gender}','danger')
            return redirect(url_for("main.index"))
        except:
            flash('There was an error submitting your form. Please ensure that the form is filled correctly!', 'danger')
            return redirect(request.referrer)

    return render_template("create_pilot.html", title="Add Pilot")


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


@users.route("/pilot/change-status-multiple/<string:action>", methods=['GET', 'POST'])
def change_status_multiple(action):
    disabled_users = []
    enabled_users = []
    input = request.form.getlist('checkbox')
    if input == None or input == [] and action == 'enable':
        message = "You havent selected what to enable."
        flash(message, 'danger')
        return redirect(request.referrer)
    elif input == None or input == [] and action == 'disable':
        message = "You havent selected what to disable."
        flash(message, 'danger')
        return redirect(request.referrer)
    else:
        checked_items = [int(x) for x in input]

        for pilot_id in checked_items:
            pilot = Pilot.query.get(pilot_id)
            if action == 'disable' and pilot.status() == 'available':
                pilot.disable()
                disabled_users.append(pilot.pilot_id)
            elif action == 'enable' and pilot.status() == 'unavailable':
                pilot.enable()
                enabled_users.append(pilot.pilot_id)
        changed_pilots_list = enabled_users if enabled_users != [] else disabled_users
        changed_pilots = " ,".join(str(pilot) for pilot in changed_pilots_list)
        message = f"Pilot(s) with ID(s)  {changed_pilots}  {action}d successfully!"
        flash(message, 'success')
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


@users.route("/pilot/delete-pilot", methods=['GET', 'POST'])
def checkbox_delete_pilots():
    if request.method == 'POST':

        deleted_pilots_list = []
        input = request.form.getlist('checkbox')
        if input == None or input == []:
            flash('You have not selected what you wish to delete. Please select an item', 'info')
            return redirect(request.referrer)
        checked_items = [int(x) for x in input]
        for pilot_id in checked_items:
            pilot = Pilot.query.get_or_404(pilot_id)
            if pilot.status() == 'available':
                message = 'Cannot deleted an enabled pilot. please first disable before you delete'
                flash(message, 'danger')
                return redirect(request.referrer)

            db.session.delete(pilot)
            deleted_pilots_list.append(pilot.pilot_id)
            deleted_pilots = ",".join(str(item) for item in deleted_pilots_list)
        db.session.commit()
        message = f"Pilots with ids {deleted_pilots} were successfully deleted from the database!"
        flash(message, 'success')
        return redirect(request.referrer)


@users.route('/flight/schedule/passenger/<int:schedule_id>', methods=['GET'])
def show_passengers(schedule_id):
    # passengers = Passenger.query.filter_by(id = schedule_id).all()
    flight_schedule = Schedule.query.get(schedule_id)
    pilots = Pilot.query.join(scheduled_pilots).join(Schedule).filter(
        (scheduled_pilots.c.pilot_id == Pilot.id) & (scheduled_pilots.c.schedule_id == schedule_id)).all()
    return render_template('passengers.html', schedule=flight_schedule, pilots=pilots)


@users.route("/show-all-pilots", methods=['POST', 'GET'])
@login_required
@admin_required
def show_all_pilots():
    pilots = Pilot.query.all()
    return render_template('pilots.html', pilots=pilots)


# @users.route("/show/<int:schedule_id>",methods = ['POST','GET'])
# def show_scheduled_pilots(schedule_id):
#     p_names = []
#     pilots = Pilot.query.join(scheduled_pilots).join(Schedule).filter((scheduled_pilots.c.pilot_id == Pilot.id) &(scheduled_pilots.c.schedule_id==schedule_id)).all()

#     for pilot in pilots:
#         p_names.append(pilot.firstname)
#     return f"{p_names}"


@users.route("/passenger/check-in/<int:passenger_id>", methods=['GET', 'POST'])
def passenger_check_in(passenger_id):
    passenger = Passenger.query.get(passenger_id)
    if passenger.status() == 'checked in':
        flash('You are already checked in', 'info')
        return redirect(url_for('main.manage_booking'))
    passenger.is_checked_in = True
    db.session.commit()
    flash('You are now checked in', 'success')
    return redirect(url_for('main.manage_booking'))


@users.route('/register-user', methods=['POST', 'GET'])
@login_required
@admin_required
def register_user():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(username=(form.username.data).capitalize(), firstname=(form.firstname.data).capitalize(),
                    lastname=(form.lastname.data).capitalize(), email=form.email.data)
        db.session.add(user)
        db.session.commit()
        # send an email containing the user reference and default password.
        flash(
            f'User {user.firstname}, {user.lastname} with  default password of {user.password} was created successfully!',
            'success')
        return redirect('/all-users')
    return render_template('users/register_user.html', form=form)


@users.route("/users/set-password", methods=['POST', 'GET'])
def set_password():
    # return "Setting password!"
    form = SetPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():

        # retrieve user with default password

        user = User.query.filter_by(password=form.default_password.data).first()

        if user:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            user.is_available = True
            db.session.commit()
            flash('Your password has been saved', 'success')
            login_user(user)
            return redirect("/user")
        flash('You password could not be set, please ensure your default password is correct', 'danger')
        return redirect('/')
    return render_template('set_password.html', form=form)


@users.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data.capitalize()
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user.is_available:
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                flash('You have logged in successfully!', 'success')
                return redirect(url_for('users.user_profile'))

            flash('Login unsuccessful, Please ensure your username and password is correct', 'danger')
            return redirect(request.referrer)
        # user needs to reset password
        if user and not user.is_available:
            flash('It appears this is your first time logging in. Please change your password', 'info')
            session["username"] = user.username
            return redirect(url_for("users.set_password"))
    return render_template('user_login.html', form=form)


@users.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    message = 'User logged out successfully'
    flash(message, 'info')
    return redirect('/')


@users.route("/user")
def user_profile():
    return render_template('users/user_profile.html')


@users.route('/all-users')
@login_required
@admin_required
def all_users():
    users = User.query.order_by(User.date_created.desc())
    return render_template('users/users.html', users=users)


@users.route("/user/<int:user_id>/make_admin", methods=["POST", "GET"])
def make_admin(user_id):
    user = User.query.get_or_404(user_id)
    # check if user is not admin and available
    if user.is_available and not user.is_admin:
        user.is_admin = True
        db.session.add(user)
        db.session.commit()
        message = "User with username {} has been made admin".format(user.username)
        flash(message, "success")
        return redirect(request.referrer)
    message = "User could not be made admin. Ensure user is available and not admin"
    flash(message, "danger")
    return redirect(request.referrer)


@users.route("/user/<int:user_id>/delete_user", methods=["POST", "GET"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user and not user.is_admin:
        db.session.delete(user)
        db.session.commit()
        message = "User {} {} with username {} deleted successfully!".format(user.firstname, user.lastname,
                                                                             user.username)
        flash(message, "info")
        return redirect(request.referrer)
    message = "Unable to delete user. Ensure user is not admin"
    flash(message, "info")
    return redirect(request.referrer)


