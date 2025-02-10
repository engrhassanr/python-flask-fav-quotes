from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, static_folder="static")

# PostgreSQL Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/quotes_db")
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
    return render_template("index.html", quotes=all_quotes)

# Quotes page - Displays form to add new quotes
@app.route("/quotes")
def quote_form():
    return render_template("quotes.html")  

# Processing the form submission
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

# Delete quote
@app.route("/delete/<int:quote_id>")
def delete_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    db.session.delete(quote)
    db.session.commit()
    return redirect(url_for("home"))

# Edit quote page
@app.route("/edit/<int:quote_id>", methods=["GET", "POST"])
def edit_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)

    if request.method == "POST":
        quote.author = request.form.get("author")
        quote.quote = request.form.get("quote")
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", quote=quote)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
