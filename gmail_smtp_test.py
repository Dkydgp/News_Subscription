import smtplib
from email.mime.text import MIMEText
import ssl

# === EDIT THESE VALUES ===
EMAIL_ADDRESS = "yourgmail@gmail.com"        # your Gmail address
APP_PASSWORD = "abcd efgh ijkl mnop"         # your Gmail App Password (remove spaces)
TO_EMAIL = "your_other_email@example.com"    # recipient for the test
# ==========================

# create the test message
msg = MIMEText("✅ Test email from your Flask newsletter project!", "plain")
msg["Subject"] = "SMTP Test Successful!"
msg["From"] = EMAIL_ADDRESS
msg["To"] = TO_EMAIL

print("📤 Connecting to Gmail SMTP...")

context = ssl.create_default_context()
try:
    # connect with SSL (port 465)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL_ADDRESS, APP_PASSWORD)
        server.send_message(msg)

    print("✅ Email sent successfully! Check your inbox or spam folder.")

except smtplib.SMTPAuthenticationError:
    print("❌ Authentication failed. Double-check your App Password or Gmail address.")
except Exception as e:
    print("🚨 Unexpected error:", e)
