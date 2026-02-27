from flask import Flask, render_template
from database import init_db
from blueprints.sport import sport_bp
from blueprints.news import news_bp
from blueprints.economics import economics_bp
from blueprints.tech import tech_bp # Importing the new blueprint

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

# Registering Blueprints
app.register_blueprint(sport_bp)
app.register_blueprint(news_bp)
app.register_blueprint(economics_bp)
app.register_blueprint(tech_bp) # Registering the tech blueprint

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    init_db()  # Initialize database on startup
    app.run(debug=True)