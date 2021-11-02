# import logging

from flight_app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="localhost", port=1234, debug=1)
