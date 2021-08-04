# from flask_imports import *
import os
import csv
from flask import Flask, render_template,request
from models import *
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("FLIGHTAPP_DB_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def main():
    db.create_all()


if __name__ == "__main__":
    with app.app_context():
        main()