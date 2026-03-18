import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'database'))

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from database import db, NewsArticle

news_bp = Blueprint("news", __name__, url_prefix="/news")


@news_bp.route("/")
def index():
    articles = NewsArticle.query.all()
    return render_template("category.html", title="News", articles=articles, category="news")


@news_bp.route("/<int:article_id>")
def detail(article_id):
    article = NewsArticle.query.get_or_404(article_id)
    return render_template("item.html", article=article, category="news")


@news_bp.route("/add", methods=["GET", "POST"])
def add():
    if not current_user.is_admin:
        flash("Admins only.", "error")
        return redirect(url_for("news.index"))

    if request.method == "POST":
        article = NewsArticle(
            title=request.form["title"],
            content=request.form["content"],
            source=request.form["source"]
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("news.index"))

    return render_template("add_article.html", title="Add News Article", category="news", extra_field="source", extra_label="Source")


@news_bp.route("/<int:article_id>/edit", methods=["GET", "POST"])
def edit(article_id):
    if not current_user.is_admin:
        flash("Admins only.", "error")
        return redirect(url_for("news.index"))

    article = NewsArticle.query.get_or_404(article_id)

    if request.method == "POST":
        article.title = request.form["title"]
        article.content = request.form["content"]
        article.source = request.form["source"]
        db.session.commit()
        return redirect(url_for("news.detail", article_id=article.id))

    return render_template("edit_article.html", article=article, category="news", extra_field="source", extra_label="Source")


@news_bp.route("/<int:article_id>/delete", methods=["POST"])
def delete(article_id):
    if not current_user.is_admin:
        flash("Admins only.", "error")
        return redirect(url_for("news.index"))

    article = NewsArticle.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for("news.index"))