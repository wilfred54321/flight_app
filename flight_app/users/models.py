from functools import wraps

from flask_login.config import EXEMPT_METHODS

from flight_app.utils import datetime, generate_default_password
from flight_app import db, login_manager
from flask import request
from flask_login import UserMixin, current_user


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, )
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_available = db.Column(db.Boolean, nullable=False, default=False)
    user_level = db.Column(db.String, nullable=False, default='standard')
    password = db.Column(db.String(100), nullable=False, default=generate_default_password)

    def status(self):
        if not self.is_available:
            return "inactive"
        return "active"

    def admin_status(self):
        if self.is_admin:
            return "Admin"
        return ""

    # def is_authenticated(self):
    #     return True

    def is_active(self):
        return self.is_available


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        if not current_user.is_admin:
            return "User must have admin privilege"
        return func(*args, **kwargs)

    return wrapper


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
