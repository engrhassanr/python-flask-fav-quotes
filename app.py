import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="static")

# Get DATABASE_URL from Railway (or default for local dev)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/quotes_db")

# Fix for "postgres://" to "postgresql://" (Railway uses "postgres://")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)

# Create tables at app startup
with app.app_context():
    db.create_all()

# Define Quote model
class Quote(db.Model):
    __tablename__ = "quotes"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    quote = db.Column(db.Text, nullable=False)

@app.route("/")
def home():
    all_quotes = Quote.query.all()
    return render_template("index.html", quotes=all_quotes)

@app.route("/quotes")
def quote_form():
    return render_template("quotes.html")  # Separate form page

@app.route("/process", methods=["POST"])
def process():
    try:
        author = request.form.get("author")
        quote_text = request.form.get("quote")

        if not author or not quote_text:
            raise ValueError("Both author and quote fields are required.")

        new_quote = Quote(author=author, quote=quote_text)
        db.session.add(new_quote)
        db.session.commit()

        return redirect(url_for("home"))

    except Exception as e:
        return render_template("quotes.html", error=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Railway PORT or fallback to 5000
    app.run(host="0.0.0.0", port=port, debug=True)