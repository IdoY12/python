from flask import Blueprint, render_template, request, redirect, url_for
from database import get_db

economics_bp = Blueprint("economics", __name__, url_prefix="/economics")

@economics_bp.route("/")
def index():
    conn = get_db()
    articles = conn.execute("SELECT * FROM economics_articles").fetchall()
    conn.close()
    return render_template("category.html", title="Economics", articles=articles, category="economics")

@economics_bp.route("/<int:article_id>")
def detail(article_id):
    conn = get_db()
    article = conn.execute(
        "SELECT * FROM economics_articles WHERE id = ?", (article_id,)
    ).fetchone()
    conn.close()
    if not article:
        return "Article not found", 404
    return render_template("item.html", article=article, category="economics")

@economics_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        sector = request.form["sector"]
        conn = get_db()
        conn.execute(
            "INSERT INTO economics_articles (title, content, sector) VALUES (?, ?, ?)",
            (title, content, sector)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("economics.index"))
    return render_template("add_article.html", title="Add Economics Article", category="economics", extra_field="sector", extra_label="Sector")