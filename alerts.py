import requests
from config import TELEGRAM_TOKEN, CHAT_ID

def send_alert(message):
    if TELEGRAM_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        return  # skip if not configured

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })