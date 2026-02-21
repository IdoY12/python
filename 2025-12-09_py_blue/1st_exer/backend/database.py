import sqlite3

DB_NAME = "app.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS sport_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            sport_type TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS news_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            source TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS economics_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            sector TEXT NOT NULL
        );
    """)

    # Inserting sample data if tables are empty
    if not cursor.execute("SELECT 1 FROM sport_articles").fetchone():
        cursor.executemany(
            "INSERT INTO sport_articles (title, content, sport_type) VALUES (?, ?, ?)",
            [
                ("Champions League", "The fourth round opened tonight with 8 thrilling matches.", "Football"),
                ("Tel Aviv Marathon", "Thousands of runners participated in the annual marathon.", "Running"),
                ("Wimbledon Tennis", "The expected final between the two greatest in the world.", "Tennis"),
            ]
        )

    if not cursor.execute("SELECT 1 FROM news_articles").fetchone():
        cursor.executemany(
            "INSERT INTO news_articles (title, content, source) VALUES (?, ?, ?)",
            [
                ("2025 Elections", "A new government will be formed following the voting results.", "ynet"),
                ("Historic Verdict", "The Supreme Court ruled on an important matter.", "Haaretz"),
                ("Weather Update", "Heavy rain is expected in the north of the country.", "Walla"),
            ]
        )

    if not cursor.execute("SELECT 1 FROM economics_articles").fetchone():
        cursor.executemany(
            "INSERT INTO economics_articles (title, content, sector) VALUES (?, ?, ?)",
            [
                ("Interest Rates Rising", "The Bank of Israel raised interest rates by 0.25%.", "Banking"),
                ("High-Tech Peak", "Israeli tech companies raised billions.", "Technology"),
                ("Housing Prices", "Housing prices rose by an average of 8% this year.", "Real Estate"),
            ]
        )

    conn.commit()
    conn.close()