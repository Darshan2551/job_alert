import feedparser
import requests
import time
import os
import threading
from flask import Flask

# ===============================
# 🌐 Flask App (Required for Render Free Web Service)
# ===============================
app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 Darshan Job Bot Running Successfully!"

# ===============================
# 🔐 Environment Variables (Render → Environment Tab)
# ===============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ===============================
# 🔎 Job Filter Keywords (Based on YOUR Skills)
# ===============================
KEYWORDS = [
    "php",
    "web developer",
    "backend",
    "javascript",
    "mysql",
    "bootstrap"
]

# RSS Feed (Indeed India)
RSS_URL = "https://in.indeed.com/rss?q=web+developer"

# ===============================
# 📩 Send Telegram Message
# ===============================
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

# ===============================
# 🔎 Check Jobs Function
# ===============================
def check_jobs():
    print("🔎 Checking new jobs...")
    feed = feedparser.parse(RSS_URL)

    for entry in feed.entries:
        title = entry.title.lower()

        if any(skill in title for skill in KEYWORDS):
            message = f"🔥 New Job Found:\n{entry.title}\n{entry.link}"
            send_telegram(message)

# ===============================
# 🔁 Background Loop
# ===============================
def run_bot():
    print("🚀 Job Bot Started...")
    while True:
        check_jobs()
        time.sleep(1800)  # every 30 minutes

# ===============================
# ▶️ Start Both Flask + Bot Thread
# ===============================
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
