# ייבוא SQLAlchemy - הספרייה שמאפשרת ORM (לעבוד עם מסד נתונים דרך Python ולא SQL גולמי)
from flask_sqlalchemy import SQLAlchemy

# יצירת אובייקט db מרכזי - יחובר לאפליקציה ב-app.py דרך db.init_app(app)
db = SQLAlchemy()


# ==================== MODELS ====================
# כל class כאן מייצג טבלה במסד הנתונים
# כל attribute מייצג עמודה בטבלה


# מודל User - טבלת המשתמשים
class User(db.Model):
    # שם הטבלה במסד הנתונים
    __tablename__ = "users"

    # עמודת id - מפתח ראשי שמקבל ערך אוטומטי
    id = db.Column(db.Integer, primary_key=True)
    # עמודת username - חייב להיות ייחודי ולא ריק
    username = db.Column(db.String(80), unique=True, nullable=False)
    # עמודת password_hash - שומרים סיסמה מוצפנת בלבד, לעולם לא גולמית
    password_hash = db.Column(db.String(200), nullable=False)
    # עמודת role - "admin" או "user", ברירת מחדל "user"
    role = db.Column(db.String(20), nullable=False, default="user")

    # property עזר - מחזיר True אם המשתמש הוא אדמין
    @property
    def is_admin(self):
        return self.role == "admin"

    # Flask-Login דורש את 4 המאפיינים הבאים בכל מודל משתמש

    # is_authenticated - האם המשתמש מחובר (תמיד True כי אם האובייקט קיים הוא מחובר)
    @property
    def is_authenticated(self):
        return True

    # is_active - האם החשבון פעיל
    @property
    def is_active(self):
        return True

    # is_anonymous - האם המשתמש אנונימי (תמיד False כי זה יוזר אמיתי)
    @property
    def is_anonymous(self):
        return False

    # get_id - Flask-Login דורש מתודה זו להחזיר את ה-ID כ-string לסשן
    def get_id(self):
        return str(self.id)


# מודל SportArticle - טבלת מאמרי ספורט
class SportArticle(db.Model):
    __tablename__ = "sport_articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # שדה ייחודי לספורט - סוג הספורט (כדורגל, ריצה וכו')
    sport_type = db.Column(db.String(100), nullable=False)


# מודל NewsArticle - טבלת מאמרי חדשות
class NewsArticle(db.Model):
    __tablename__ = "news_articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # שדה ייחודי לחדשות - מקור הידיעה (ynet, haaretz וכו')
    source = db.Column(db.String(100), nullable=False)


# מודל EconomicsArticle - טבלת מאמרי כלכלה
class EconomicsArticle(db.Model):
    __tablename__ = "economics_articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # שדה ייחודי לכלכלה - סקטור (בנקאות, נדל"ן וכו')
    sector = db.Column(db.String(100), nullable=False)


# מודל TechArticle - טבלה חדשה לטכנולוגיה (לא הייתה קודם)
class TechArticle(db.Model):
    __tablename__ = "tech_articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # שדה ייחודי לטכנולוגיה - תחום הטכנולוגיה (AI, Hardware וכו')
    tech_field = db.Column(db.String(100), nullable=False)


# ==================== INIT ====================

def init_db(app):
    # יצירת כל הטבלאות אם לא קיימות, ואז הכנסת נתוני דוגמה
    with app.app_context():
        # create_all - סורק את כל המודלים ויוצר טבלאות אם לא קיימות
        db.create_all()
        # קריאה לפונקציה שמכניסה נתוני דוגמה
        _seed_data()


def _seed_data():
    # הכנסת נתוני דוגמה רק אם הטבלאות ריקות

    # .query.first() - שאילתת ORM שמחזירה את השורה הראשונה, None אם ריק
    if not SportArticle.query.first():
        # db.session.add_all - הוספת מספר אובייקטים בבת אחת
        db.session.add_all([
            SportArticle(title="Champions League", content="The fourth round opened tonight with 8 thrilling matches.", sport_type="Football"),
            SportArticle(title="Tel Aviv Marathon", content="Thousands of runners participated in the annual marathon.", sport_type="Running"),
            SportArticle(title="Wimbledon Tennis", content="The expected final between the two greatest in the world.", sport_type="Tennis"),
        ])

    if not NewsArticle.query.first():
        db.session.add_all([
            NewsArticle(title="2025 Elections", content="A new government will be formed following the voting results.", source="ynet"),
            NewsArticle(title="Historic Verdict", content="The Supreme Court ruled on an important matter.", source="Haaretz"),
            NewsArticle(title="Weather Update", content="Heavy rain is expected in the north of the country.", source="Walla"),
        ])

    if not EconomicsArticle.query.first():
        db.session.add_all([
            EconomicsArticle(title="Interest Rates Rising", content="The Bank of Israel raised interest rates by 0.25%.", sector="Banking"),
            EconomicsArticle(title="High-Tech Peak", content="Israeli tech companies raised billions.", sector="Technology"),
            EconomicsArticle(title="Housing Prices", content="Housing prices rose by an average of 8% this year.", sector="Real Estate"),
        ])

    if not TechArticle.query.first():
        db.session.add_all([
            TechArticle(title="AI Revolution", content="Large language models are changing the software industry.", tech_field="Artificial Intelligence"),
            TechArticle(title="Apple Vision Pro", content="Apple's spatial computing headset ships to developers.", tech_field="Hardware"),
            TechArticle(title="Python 4.0", content="The Python community debates the next major version.", tech_field="Programming"),
        ])

    # db.session.commit() - שמירת כל השינויים למסד הנתונים (כמו conn.commit() ב-sqlite3)
    db.session.commit()