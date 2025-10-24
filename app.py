from flask import Flask, render_template, request, jsonify
import pymysql
import datetime

app = Flask(__name__)

# ✅ Replace these with your own FreeSQLDatabase credentials
DB_HOST = "sql12.freesqldatabase.com"
DB_USER = "sql12804263"
DB_PASS = "HZde2xMXSR"
DB_NAME = "sql12804263"

# Function to connect to MySQL database
def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# Home route (renders HTML page)
@app.route('/')
def home():
    return render_template('index.html')

# Subscription API route
@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"status": "error", "message": "Email is required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO subscribers (email, subscribed_at) VALUES (%s, %s)"
        cursor.execute(sql, (email, datetime.datetime.now()))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "message": "✅ Subscribed successfully!"})
    except pymysql.err.IntegrityError:
        return jsonify({"status": "error", "message": "⚠️ This email is already subscribed."}), 400
    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": "❌ Database error occurred."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
