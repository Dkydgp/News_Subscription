from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow your frontend to connect

subscribers = []  # temporary list (later we’ll use SQLite or Firebase)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    email = data.get("email")
    if email:
        subscribers.append(email)
        print("✅ New subscriber:", email)
        return jsonify({"message": "Subscribed successfully!"}), 200
    return jsonify({"error": "No email provided"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)