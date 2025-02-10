from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, static_folder="static")

# Use DATABASE_URL from the environment, fallback to local PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/quotes_db")

# Ensure compatibility with Heroku (sometimes DATABASE_URL starts with 'postgres://')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)

# Define Quote model
class Quote(db.Model):
    __tablename__ = "quotes"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    quote = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Quote {self.id} - {self.author}>"

# Create database tables
with app.app_context():
    db.create_all()

# Home page - Displays all quotes
@app.route("/")
def home():
    all_quotes = Quote.query.all()
    print(f"Fetched Quotes: {all_quotes}")  # Debugging
    return render_template("index.html", quotes=all_quotes)

# Quotes page - Displays form to add new quotes
@app.route("/quotes")
def quote_form():
    return render_template("quotes.html")  # Separate form page

# Processing the form submission
@app.route("/process", methods=["POST"])
def process():
    try:
        author = request.form.get("author")
        quote_text = request.form.get("quote")

        print(f"Received: Author - {author}, Quote - {quote_text}")  # Debugging

        if not author or not quote_text:
            raise ValueError("Both author and quote fields are required.")

        new_quote = Quote(author=author, quote=quote_text)
        db.session.add(new_quote)
        db.session.commit()

        print("Quote saved successfully!")  # Debugging

        return redirect(url_for("home"))  # Redirect to home page

    except Exception as e:
        print(f"Error: {e}")  
        return render_template("quotes.html", error=str(e))  # Show error on form page


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Railway provides a PORT
    app.run(host="0.0.0.0", port=port, debug=True)

