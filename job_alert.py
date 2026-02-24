import feedparser
import requests
import time
import os

# 🔐 Use ENV variables (important for Render security)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

KEYWORDS = ["php", "web developer", "backend", "javascript", "mysql", "bootstrap"]

RSS_URL = "https://in.indeed.com/rss?q=web+developer"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

def check_jobs():
    feed = feedparser.parse(RSS_URL)

    for entry in feed.entries:
        title = entry.title.lower()

        if any(skill in title for skill in KEYWORDS):
            message = f"🔥 New Job Found:\n{entry.title}\n{entry.link}"
            send_telegram(message)

# 🔁 Infinite loop for Render worker
while True:
    check_jobs()
    time.sleep(1800)  # every 30 minutes