# emailer.py
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# -----------------------------
# Recipients list
# -----------------------------
recipients = [
   # "mhasan06@gmail.com",
    "mohammad.hasan@a2baustralia.com"
]

# -----------------------------
# Send list of articles via email
# -----------------------------
def send_articles_email(articles, subject="🚖 Taxi News"):
    """
    Send a list of articles via email to all recipients.    
    Each article should have: title, summary, impact, company (optional), link
    """
    if not articles:
        print("No articles to send.")
        return

    sender_email = "mhasan06@gmail.com"      # Replace with your Gmail
    app_password = "pptnqvgatgghnxfd"        # Gmail App Password

    # Build HTML content
    html = f"<h2>{subject}</h2>"
    for item in articles:
        html += f"""
        <p>
            <b>{item['title']}</b><br>
            🧠 {item['summary']}<br>
            📊 Impact: {item['impact']}<br>
        """
        if item.get("company"):
            html += f"🏢 Company: {item['company']}<br>"
        html += f'<a href="{item["link"]}">Read more</a></p><hr>'

    # Send email to all recipients
    for recipient_email in recipients:
        msg = MIMEText(html, "html")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, app_password)
                server.send_message(msg)
            print(f"✅ Email sent to {recipient_email}")
        except Exception as e:
            print(f"❌ Failed to send to {recipient_email}: {e}")


# -----------------------------
# Helper functions
# -----------------------------
def send_company_alerts(articles):
    """Send only company-related alerts"""
    alerts = [a for a in articles if a.get("company")]
    send_articles_email(alerts, subject="🚨 Taxi Company Alerts")

def send_last_24h_articles(articles):
    """Send all articles from the last 24 hours"""
    now = datetime.utcnow()
    last_24h = [a for a in articles if (now - a["published"]) < timedelta(hours=24)]
    send_articles_email(last_24h, subject="🟢 Taxi News - Last 24 Hours")
