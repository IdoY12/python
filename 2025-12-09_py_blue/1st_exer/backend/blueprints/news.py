from flask import Blueprint, render_template, request, redirect, url_for
from database import get_db

news_bp = Blueprint("news", __name__, url_prefix="/news")

@news_bp.route("/")
def index():
    conn = get_db()
    articles = conn.execute("SELECT * FROM news_articles").fetchall()
    conn.close()
    return render_template("category.html", title="News", articles=articles, category="news")

@news_bp.route("/<int:article_id>")
def detail(article_id):
    conn = get_db()
    article = conn.execute(
        "SELECT * FROM news_articles WHERE id = ?", (article_id,)
    ).fetchone()
    conn.close()
    if not article:
        return "Article not found", 404
    return render_template("item.html", article=article, category="news")

@news_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        source = request.form["source"]
        conn = get_db()
        conn.execute(
            "INSERT INTO news_articles (title, content, source) VALUES (?, ?, ?)",
            (title, content, source)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("news.index"))
    return render_template("add_article.html", title="Add News Article", category="news", extra_field="source", extra_label="Source")