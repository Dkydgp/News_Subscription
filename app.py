from flask import Flask, jsonify
from flask_mail import Mail, Message
import pymysql
import requests

app = Flask(__name__)

# ------------------ 🔧 CONFIG ------------------
# Gmail SMTP settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'YOUR_GMAIL@gmail.com'  # change this
app.config['MAIL_PASSWORD'] = 'YOUR_APP_PASSWORD'      # use Gmail App Password (not normal password)
app.config['MAIL_DEFAULT_SENDER'] = ('MyPA Newsletter', 'YOUR_GMAIL@gmail.com')

# FreeSQLDatabase connection
DB_HOST = 'sql12.freesqldatabase.com'
DB_USER = 'sql12804263'
DB_PASS = 'HZde2xMXSR'
DB_NAME = 'sql12804263'

# News API (example: newsapi.org)
NEWS_API_KEY = 'YOUR_NEWSAPI_KEY'
NEWS_API_URL = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}'

mail = Mail(app)
# ------------------------------------------------

def get_top_news():
    """Fetch Top 5 News Articles"""
    try:
        res = requests.get(NEWS_API_URL)
        data = res.json()
        articles = data.get('articles', [])[:5]
        
        html = "<h2>🗞️ Top 5 News Today</h2><ul>"
        for n in articles:
            title = n.get('title', 'No title')
            url = n.get('url', '#')
            source = n.get('source', {}).get('name', 'Unknown')
            html += f"<li><b>{title}</b> — {source}<br><a href='{url}'>Read more</a></li>"
        html += "</ul><hr><p>This message was sent automatically by MyPA Newsletter System.</p>"
        return html
    except Exception as e:
        print("Error fetching news:", e)
        return None


def get_subscribers():
    """Fetch all subscriber emails from FreeSQLDatabase"""
    try:
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM subscribers WHERE email IS NOT NULL;")
        emails = [row[0] for row in cursor.fetchall()]
        conn.close()
        return emails
    except Exception as e:
        print("Error connecting to database:", e)
        return []


def send_newsletter():
    """Send the top 5 news to all subscribers"""
    html_content = get_top_news()
    if not html_content:
        return "❌ Failed to fetch news."

    emails = get_subscribers()
    if not emails:
        return "❌ No subscribers found."

    with mail.connect() as conn:
        for email in emails:
            try:
                msg = Message(subject="🗞️ Top 5 News - Daily Digest", recipients=[email], html=html_content)
                conn.send(msg)
                print(f"✅ Sent to {email}")
            except Exception as e:
                print(f"❌ Failed to send to {email}:", e)
    return f"✅ Newsletter sent to {len(emails)} subscribers."


@app.route('/send-news', methods=['GET'])
def send_news():
    """HTTP route to trigger sending manually"""
    result = send_newsletter()
    return jsonify({"message": result})


if __name__ == '__main__':
    app.run(debug=True)
