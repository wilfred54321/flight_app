from flask_imports import *

app = Flask(__name__)

@app.route("/")
def index():
    greeting = "Hello, World"
    return render_template("index.html",greeting=greeting)