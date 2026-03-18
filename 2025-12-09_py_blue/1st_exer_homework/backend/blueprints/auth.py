import sys
import os

# הוספת תיקיית database ל-path כדי שנוכל לייבא ממנה
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'database'))

from flask import Blueprint, render_template, request, redirect, url_for, flash
# generate_password_hash - מצפין סיסמה לפני שמירה
# check_password_hash - משווה סיסמה גולמית לסיסמה מוצפנת שמורה
from werkzeug.security import generate_password_hash, check_password_hash
# login_user - מחבר יוזר לסשן אחרי לוגין מוצלח
# logout_user - מנתק יוזר מהסשן
# login_required - דקורטור שחוסם גישה למי שלא מחובר
from flask_login import login_user, logout_user, login_required

# ייבוא db ומודל User מ-database.py
from database import db, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# ==================== REGISTER ====================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # request.form.get עם ברירת מחדל - אם לא נשלח role, ברירת מחדל היא "user"
        role = request.form.get("role", "user")

        # בדיקה אם שם המשתמש כבר קיים - ORM במקום SELECT
        if User.query.filter_by(username=username).first():
            # flash - שולח הודעה חד פעמית שתוצג ב-base.html
            flash("Username already exists", "error")
            return redirect(url_for("auth.register"))

        # generate_password_hash - מצפין את הסיסמה, לעולם לא שומרים סיסמה גולמית
        hashed = generate_password_hash(password)

        # יצירת אובייקט User חדש ושמירה למסד - ORM במקום INSERT INTO
        new_user = User(username=username, password_hash=hashed, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("Registered successfully! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ==================== LOGIN ====================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # חיפוש יוזר לפי שם משתמש - ORM במקום SELECT WHERE
        user = User.query.filter_by(username=username).first()

        # check_password_hash - משווה את הסיסמה שהוזנה לסיסמה המוצפנת שמורה
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid username or password", "error")
            return redirect(url_for("auth.login"))

        # login_user - שומר את פרטי היוזר בסשן
        login_user(user)
        flash(f"Welcome, {user.username}!", "success")
        return redirect(url_for("home"))

    return render_template("login.html")


# ==================== LOGOUT ====================

@auth_bp.route("/logout")
# login_required - רק מי שמחובר יכול להתנתק
@login_required
def logout():
    # logout_user - מוחק את פרטי היוזר מהסשן
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("home"))