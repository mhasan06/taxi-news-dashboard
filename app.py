# app.py
import streamlit as st
from scraper import scrape_news_rss_au
from emailer import send_last_24h_articles
from datetime import datetime, timedelta
from collections import defaultdict
from streamlit_autorefresh import st_autorefresh
import subprocess

# -----------------------------
# Auto-refresh every 10 minutes
# -----------------------------
st_autorefresh(interval=600000, key="refresh")

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="Taxi News AU", layout="wide")
st.title("🚖 Australian Taxi / Rideshare News Dashboard")

# -----------------------------
# Last refreshed & version
# -----------------------------
st.caption(f"🕒 Last updated: {datetime.now().strftime('%d %b %Y %I:%M %p')}")
# Show git commit version (optional)
try:
    commit = subprocess.getoutput("git rev-parse --short HEAD")
    st.caption(f"App version: {commit}")
except:
    pass

# -----------------------------
# Fetch articles
# -----------------------------
articles = scrape_news_rss_au()

# -----------------------------
# Filter last 24 hours
# -----------------------------
now = datetime.utcnow()
last_24h = [a for a in articles if (now - a["published"]) < timedelta(hours=24)]

# -----------------------------
# Sidebar: sections
# -----------------------------
section = st.sidebar.radio(
    "Select News Section",
    ("🔥 Top News", "🟢 Last 24h", "🗺️ State News")
)

# -----------------------------
# Top news (latest 3)
# -----------------------------
if section == "🔥 Top News":
    st.header("🔥 Top 3 Latest News")
    top_articles = sorted(last_24h, key=lambda x: x["published"], reverse=True)[:3]
    for item in top_articles:
        st.subheader(item["title"])
        st.write(f"📅 {item['published']} | 📰 {item['source']} | 📍 {item['state']}")
        if item.get("company"):
            st.write(f"🏢 {item['company']}")
        st.markdown(f"[Read more]({item['link']})")
        st.markdown("---")

# -----------------------------
# Last 24 hours
# -----------------------------
elif section == "🟢 Last 24h":
    st.header("🟢 News from the Last 24 Hours")
    for item in last_24h:
        st.subheader(item["title"])
        st.write(f"📅 {item['published']} | 📰 {item['source']} | 📍 {item['state']}")
        if item.get("company"):
            st.write(f"🏢 {item['company']}")
        st.markdown(f"[Read more]({item['link']})")
        st.markdown("---")

# -----------------------------
# State News
# -----------------------------
elif section == "🗺️ State News":
    st.header("🗺️ State News")
    state_news = [a for a in last_24h if a["state"] != "National"]
    states = defaultdict(list)
    for article in state_news:
        states[article["state"]].append(article)
    for state, items in states.items():
        st.subheader(f"📍 {state}")
        for item in items:
            st.write(f"📅 {item['published']} | 📰 {item['source']}")
            if item.get("company"):
                st.write(f"🏢 {item['company']}")
            st.write(item["title"])
            st.markdown(f"[Read more]({item['link']})")
            st.markdown("---")

# -----------------------------
# Footer: developer credit
# -----------------------------
st.markdown('<p style="text-align:right; font-size:12px;">Developed by Mohammad Hasan</p>', unsafe_allow_html=True)