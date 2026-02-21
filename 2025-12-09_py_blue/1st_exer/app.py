from flask import Flask, render_template
from database import init_db
from blueprints.sport import sport_bp
from blueprints.news import news_bp
from blueprints.economics import economics_bp

app = Flask(__name__)

# Registering Blueprints
app.register_blueprint(sport_bp)
app.register_blueprint(news_bp)
app.register_blueprint(economics_bp)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    init_db()  # Creates tables and sample data on first run
    app.run(debug=True)