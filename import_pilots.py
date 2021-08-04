import os
import csv
from flask import Flask, render_template,request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("FLIGHTAPP_DB_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def main():
    with open('pilots.csv') as file:
        pilots = csv.reader(file)
        print(type(pilots))
        for firstname,lastname,id_number in pilots:
            pilot = Pilot(firstname = firstname, 
            lastname = lastname, id_number = id_number)
            db.session.add(pilot)
        print(f"Added pilot {firstname} {lastname} to the database!")
    db.session.commit()
        
if __name__ == "__main__":
    with app.app_context():
        main()

