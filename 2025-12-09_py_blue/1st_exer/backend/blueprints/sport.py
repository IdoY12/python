from flask import Blueprint, render_template, request, redirect, url_for
from database import get_db

sport_bp = Blueprint("sport", __name__, url_prefix="/sport")

# Endpoint 1: List of all articles
@sport_bp.route("/")
def index():
    conn = get_db()
    articles = conn.execute("SELECT * FROM sport_articles").fetchall()
    conn.close()
    return render_template("category.html", title="Sport", articles=articles, category="sport")

# Endpoint 2: Single article by ID
@sport_bp.route("/<int:article_id>")
def detail(article_id):
    conn = get_db()
    article = conn.execute(
        "SELECT * FROM sport_articles WHERE id = ?", (article_id,)
    ).fetchone()
    conn.close()
    if not article:
        return "Article not found", 404
    return render_template("item.html", article=article, category="sport")

# Endpoint 3: Adding a new article
@sport_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        sport_type = request.form["sport_type"]
        conn = get_db()
        conn.execute(
            "INSERT INTO sport_articles (title, content, sport_type) VALUES (?, ?, ?)",
            (title, content, sport_type)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("sport.index"))
    return render_template("add_article.html", title="Add Sport Article", category="sport", extra_field="sport_type", extra_label="Sport Type")