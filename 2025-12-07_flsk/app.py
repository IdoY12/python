from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/main")
def test():
    return render_template('main.html')

@app.route("/hello", methods=['GET', 'POST'])
def hello():
    return render_template('hello.html')
