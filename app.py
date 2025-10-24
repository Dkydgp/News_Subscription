# ============================================================
#  Email Newsletter Flask Backend  |  Compatible with Flask 3+
# ============================================================

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# ------------------------------------------------------------
#  1. Load environment variables (Render will inject DB_URI)
# ------------------------------------------------------------
load_dotenv()

app = Flask(__name__)
CORS(app)  # allow frontend to call this API from any domain

# ------------------------------------------------------------
#  2. Configure database connection
# ------------------------------------------------------------
# Example value in Render Environment Variables:
# DB_URI = mysql+pymysql://sql12804263:HZde2xMXSR@sql12.freesqldatabase.com:3306/sql12804263
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ------------------------------------------------------------
#  3. Define database model
# ------------------------------------------------------------
class Subscriber(db.Model):
    __tablename__ = "subscribers"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<Subscriber {self.email}>"

# ------------------------------------------------------------
#  4. Routes
# ------------------------------------------------------------
@app.route("/")
def home():
    """Serve the HTML subscription page."""
    return render_template("index.html")


@app.route("/subscribe", methods=["POST"])
def subscribe():
    """Handle newsletter form submissions."""
    data = request.get_json() or {}
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Check for duplicates
    existing = Subscriber.query.filter_by(email=email).first()
    if existing:
        return jsonify({"message": "Already subscribed!"}), 200

    # Save new subscriber
    new_subscriber = Subscriber(email=email)
    db.session.add(new_subscriber)
    db.session.commit()

    print(f"✅ New subscriber saved: {email}")
    return jsonify({"message": "Subscribed successfully!"}), 200


@app.route("/ping")
def ping():
    """Simple health-check endpoint."""
    return jsonify({"status": "ok"}), 200

# ------------------------------------------------------------
#  5. Initialize database (Flask 3+ safe)
# ------------------------------------------------------------
with app.app_context():
    db.create_all()
    print("✅ Database tables verified/created")

# ------------------------------------------------------------
#  6. Run app locally (Render uses gunicorn to start this)
# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
