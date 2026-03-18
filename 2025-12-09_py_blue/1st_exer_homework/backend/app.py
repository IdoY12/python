import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'database'))

from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, current_user
from database import db, init_db, User

from blueprints.sport import sport_bp
from blueprints.news import news_bp
from blueprints.economics import economics_bp
from blueprints.tech import tech_bp
from blueprints.auth import auth_bp

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

app.config["SECRET_KEY"] = "your-secret-key-change-this"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'database', 'app.db')
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.register"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(sport_bp)
app.register_blueprint(news_bp)
app.register_blueprint(economics_bp)
app.register_blueprint(tech_bp)
app.register_blueprint(auth_bp)

# ==================== BEFORE REQUEST ====================
# הפונקציה הזו רצה לפני כל בקשה שמגיעה לשרת - ללא יוצא מן הכלל
# זה ה-enforceAuth המרכזי - במקום לשים @login_required על כל פונקציה בנפרד
@app.before_request
def require_login():
    # הרשימה הלבנה - הדפים היחידים שמותר לגשת אליהם בלי להיות מחובר
    # "auth.login"    = הפונקציה login בבלופרינט auth (/auth/login)
    # "auth.register" = הפונקציה register בבלופרינט auth (/auth/register)
    # "static"        = קבצי CSS/JS/תמונות - חייב להיות פתוח אחרת העיצוב לא יטען
    allowed = ["auth.login", "auth.register", "static"]

    # request.endpoint = שם הפונקציה שהבקשה הולכת אליה
    # למשל בקשה ל-/sport/ תיתן endpoint = "sport.index"
    # בקשה ל-/auth/login תיתן endpoint = "auth.login"

    # אם הבקשה הולכת לדף שלא ברשימה הלבנה, והמשתמש לא מחובר - חוסמים
    if request.endpoint not in allowed and not current_user.is_authenticated:
        return redirect(url_for("auth.register"))

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    init_db(app)
    app.run(debug=True)