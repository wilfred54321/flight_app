class Flight:
    def __init__(self, capacity):
        self.capacity = capacity
        self.passengers = []

    def add_passenger(self, name):
        if not self.open_seats():
            return False
        self.passengers.append(name)
        return False

    def open_seats(self):
        return self.capacity - len(self.passengers)


flight = Flight(3)
passengers = ["Wilfred", "ThankGod", "Godwin", "Frankin"]

for passenger in passengers:
    if flight.open_seats():
        flight.add_passenger(passenger)
        print(f"Passenger with name {passenger} added to flight")
    else:
        print(
            f"No seats avaialable for {passenger}. Please wait for the next available flight"
        )
print(f"Total avaialable seats are {flight.open_seats()}")
