import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'database'))

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from database import db, TechArticle

tech_bp = Blueprint("tech", __name__, url_prefix="/tech")


@tech_bp.route("/")
def index():
    articles = TechArticle.query.all()
    return render_template("tech_special.html", articles=articles)


@tech_bp.route("/<int:article_id>")
def detail(article_id):
    article = TechArticle.query.get_or_404(article_id)
    return render_template("item.html", article=article, category="tech")


@tech_bp.route("/add", methods=["GET", "POST"])
def add():
    if not current_user.is_admin:
        flash("Admins only.", "error")
        return redirect(url_for("tech.index"))

    if request.method == "POST":
        article = TechArticle(
            title=request.form["title"],
            content=request.form["content"],
            tech_field=request.form["tech_field"]
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("tech.index"))

    return render_template("add_article.html", title="Add Tech Article", category="tech", extra_field="tech_field", extra_label="Tech Field")


@tech_bp.route("/<int:article_id>/edit", methods=["GET", "POST"])
def edit(article_id):
    if not current_user.is_admin:
        flash("Admins only.", "error")
        return redirect(url_for("tech.index"))

    article = TechArticle.query.get_or_404(article_id)

    if request.method == "POST":
        article.title = request.form["title"]
        article.content = request.form["content"]
        article.tech_field = request.form["tech_field"]
        db.session.commit()
        return redirect(url_for("tech.detail", article_id=article.id))

    return render_template("edit_article.html", article=article, category="tech", extra_field="tech_field", extra_label="Tech Field")


@tech_bp.route("/<int:article_id>/delete", methods=["POST"])
def delete(article_id):
    if not current_user.is_admin:
        flash("Admins only.", "error")
        return redirect(url_for("tech.index"))

    article = TechArticle.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for("tech.index"))