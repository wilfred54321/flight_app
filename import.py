from flask_imports import *
import csv

def main():
    with open("flights.csv") as file:
        data = csv.reader(file)
        for code,origin,destination,capacity,duration in data:
            flight = Flight(code = code, origin = origin, 
            destination = destination, capacity = capacity,
            duration = duration)
            db.session.add(flight)
            print(f"Added flight {code} from {origin} to {destination}lasting {duration}")
    db.session.commit()


if __name__ == "__main__":
    main()


