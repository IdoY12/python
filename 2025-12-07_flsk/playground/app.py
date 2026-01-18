from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)

# Allow cross-origin requests from all origins
CORS(app)

@app.route("/")
def hello_world():
    my_tasks = ["buy milk", "finish the project", "go to the gym"]
    return my_tasks

