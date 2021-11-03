from flask import Flask
import os
from flight_app.models import db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("FLIGHTAPP_DB_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SECRET_KEY"] = "dfe56e985611aa6f"

    db.init_app(app)

    from .main.routes import main
    from .users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)

    return app
