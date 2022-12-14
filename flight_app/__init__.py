from flask import Flask
import logging

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

logging.basicConfig(level=logging.DEBUG)
login_manager = LoginManager()
db = SQLAlchemy()
bcrypt = Bcrypt()




def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flight_app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SECRET_KEY"] = "dfe56e985611aa6f"

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from .main.routes import main
    from .users.routes import users
    from .flight.routes import flight
    from.schedule.routes import schedule

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(flight)
    app.register_blueprint(schedule)

    return app
