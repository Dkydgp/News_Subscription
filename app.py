from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables (for local use; Render will inject them automatically)
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database URI comes from Render environment variable (secure)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ====== Model ======
class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<Subscriber {self.email}>"

# ====== Routes ======
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    existing = Subscriber.query.filter_by(email=email).first()
    if existing:
        return jsonify({"message": "Already subscribed!"}), 200

    new_subscriber = Subscriber(email=email)
    db.session.add(new_subscriber)
    db.session.commit()
    print(f"✅ New subscriber saved: {email}")
    return jsonify({"message": "Subscribed successfully!"}), 200

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
