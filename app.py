from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import pymysql
import requests
import os

app = Flask(__name__)

# ------------------ CONFIG ------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('MyPA Newsletter', os.getenv('MAIL_USERNAME'))

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

mail = Mail(app)
# ------------------------------------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if not email:
        return "Email is required!", 400

    try:
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO subscribers (email) VALUES (%s)", (email,))
        conn.commit()
        conn.close()
    except Exception as e:
        print("DB Error:", e)
        return "Something went wrong.", 500

    return render_template('success.html')

def get_top_news():
    url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}'
    res = requests.get(url)
    articles = res.json().get('articles', [])[:5]
    html = "<h2>🗞 Top 5 News Today</h2><ul>"
    for n in articles:
        html += f"<li><b>{n.get('title')}</b><br><a href='{n.get('url')}'>Read more</a></li>"
    html += "</ul><hr><p>Sent automatically by MyPA Newsletter System.</p>"
    return html

@app.route('/send-news', methods=['GET'])
def send_news():
    """Send newsletter to all subscribers"""
    html = get_top_news()
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM subscribers WHERE email IS NOT NULL;")
    emails = [row[0] for row in cursor.fetchall()]
    conn.close()

    with mail.connect() as conn_mail:
        for e in emails:
            msg = Message(subject="🗞️ Top 5 News - Daily Digest", recipients=[e], html=html)
            conn_mail.send(msg)
            print("✅ Sent to:", e)
    return jsonify({"message": f"Newsletter sent to {len(emails)} subscribers."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
