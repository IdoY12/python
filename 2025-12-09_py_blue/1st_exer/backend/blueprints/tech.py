from flask import Blueprint, render_template, request, redirect, url_for
from database import get_db

tech_bp = Blueprint("tech", __name__, url_prefix="/tech")

@tech_bp.route("/")
def index():
    conn = get_db()
    # Pulling from economics because tech_articles doesn't exist yet
    articles = conn.execute("SELECT * FROM economics_articles").fetchall()
    conn.close()
    
    return render_template("tech_special.html", articles=articles)