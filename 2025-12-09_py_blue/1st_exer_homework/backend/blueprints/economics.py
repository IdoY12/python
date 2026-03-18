import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'database'))

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from database import db, EconomicsArticle

economics_bp = Blueprint("economics", __name__, url_prefix="/economics")


@economics_bp.route("/")
def index():
    articles = EconomicsArticle.query.all()
    return render_template("category.html", title="Economics", articles=articles, category="economics")


@economics_bp.route("/<int:article_id>")
def detail(article_id):
    article = EconomicsArticle.query.get_or_404(article_id)
    return render_template("item.html", article=article, category="economics")


@economics_bp.route("/add", methods=["GET", "POST"])
def add():
    if not current_user.is_admin:
        flash("Admins only.", "error")
        return redirect(url_for("economics.index"))

    if request.method == "POST":
        article = EconomicsArticle(
            title=request.form["title"],
            content=request.form["content"],
            sector=request.form["sector"]
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("economics.index"))

    return render_template("add_article.html", title="Add Economics Article", category="economics", extra_field="sector", extra_label="Sector")


@economics_bp.route("/<int:article_id>/edit", methods=["GET", "POST"])
def edit(article_id):
    if not current_user.is_admin:
        flash("Admins only.", "error")
        return redirect(url_for("economics.index"))

    article = EconomicsArticle.query.get_or_404(article_id)

    if request.method == "POST":
        article.title = request.form["title"]
        article.content = request.form["content"]
        article.sector = request.form["sector"]
        db.session.commit()
        return redirect(url_for("economics.detail", article_id=article.id))

    return render_template("edit_article.html", article=article, category="economics", extra_field="sector", extra_label="Sector")


@economics_bp.route("/<int:article_id>/delete", methods=["POST"])
def delete(article_id):
    if not current_user.is_admin:
        flash("Admins only.", "error")
        return redirect(url_for("economics.index"))

    article = EconomicsArticle.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for("economics.index"))