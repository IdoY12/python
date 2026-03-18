import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'database'))

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from database import db, SportArticle

sport_bp = Blueprint("sport", __name__, url_prefix="/sport")


@sport_bp.route("/")
def index():
    # before_request כבר בדק שהמשתמש מחובר לפני שהגענו לכאן
    articles = SportArticle.query.all()
    return render_template("category.html", title="Sport", articles=articles, category="sport")


@sport_bp.route("/<int:article_id>")
def detail(article_id):
    # before_request כבר בדק שהמשתמש מחובר לפני שהגענו לכאן
    article = SportArticle.query.get_or_404(article_id)
    return render_template("item.html", article=article, category="sport")


@sport_bp.route("/add", methods=["GET", "POST"])
def add():
    # before_request בדק שמחובר, כאן בודקים גם שהוא אדמין
    if not current_user.is_admin:
        flash("Admins only.", "error")
        return redirect(url_for("sport.index"))

    if request.method == "POST":
        article = SportArticle(
            title=request.form["title"],
            content=request.form["content"],
            sport_type=request.form["sport_type"]
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("sport.index"))

    return render_template("add_article.html", title="Add Sport Article", category="sport", extra_field="sport_type", extra_label="Sport Type")


@sport_bp.route("/<int:article_id>/edit", methods=["GET", "POST"])
def edit(article_id):
    if not current_user.is_admin:
        flash("Admins only.", "error")
        return redirect(url_for("sport.index"))

    article = SportArticle.query.get_or_404(article_id)

    if request.method == "POST":
        article.title = request.form["title"]
        article.content = request.form["content"]
        article.sport_type = request.form["sport_type"]
        db.session.commit()
        return redirect(url_for("sport.detail", article_id=article.id))

    return render_template("edit_article.html", article=article, category="sport", extra_field="sport_type", extra_label="Sport Type")


@sport_bp.route("/<int:article_id>/delete", methods=["POST"])
def delete(article_id):
    if not current_user.is_admin:
        flash("Admins only.", "error")
        return redirect(url_for("sport.index"))

    article = SportArticle.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for("sport.index"))