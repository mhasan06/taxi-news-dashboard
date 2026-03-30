# app.py
import streamlit as st
from scraper import scrape_news_rss_au
from collections import defaultdict
from datetime import datetime, timedelta
from emailer import send_company_alerts, send_last_24h_articles

# -----------------------------
# Streamlit page config
# -----------------------------
st.set_page_config(page_title="Taxi News AU", layout="wide")
st.title("🚖  A2B Australia - Taxi and Rideshare News Alerts")

# -----------------------------
# Scrape articles
# -----------------------------
articles = scrape_news_rss_au()
now = datetime.utcnow()

# -----------------------------
# Time filters
# -----------------------------
def in_last_hours(article, hours):
    return (now - article["published"]) < timedelta(hours=hours)

new_24h = [a for a in articles if in_last_hours(a, 24)]
recent_3d = [a for a in articles if in_last_hours(a, 72)]

alerts = [a for a in articles if a.get("company")]

# -----------------------------
# Sidebar
# -----------------------------
section = st.sidebar.radio(
    "Select Section",
    ("🔥 Top News", "🟢 Last 24h", "🟡 Last 3 Days", "🚨 Company Alerts", "🗺️ State News")
)

top_n = st.sidebar.slider("Top N articles", 1, 10, 5)

# Buttons to send emails
if st.sidebar.button("📧 Send Last 24h Articles"):
    send_last_24h_articles(articles)
    st.success("Last 24h articles sent to all recipients!")

if st.sidebar.button("🚨 Send Company Alerts"):
    send_company_alerts(articles)
    st.success("Company alerts sent to all recipients!")

# -----------------------------
# Display articles
# -----------------------------
def show_articles(article_list):
    if not article_list:
        st.write("No articles found.")
        return
    for item in article_list:
        st.subheader(item["title"])
        st.write(f"📅 {item['published']} | 📰 {item['source']} | 📍 {item['state']}")
        st.write(f"🧠 {item['summary']}")
        impact = item.get("impact", "Unknown")
        if impact == "Positive":
            st.success(f"📊 Impact: {impact}")
        elif impact == "Negative":
            st.error(f"📊 Impact: {impact}")
        else:
            st.info(f"📊 Impact: {impact}")
        if item.get("company"):
            st.warning(f"🏢 Company Alert: {item['company']}")
        st.markdown(f"[Read more]({item['link']})")
        st.markdown("---")

# -----------------------------
# Sections
# -----------------------------
if section == "🔥 Top News":
    st.header("🔥 Top News (Latest 24h)")
    top_articles = sorted(new_24h, key=lambda x: x["published"], reverse=True)[:top_n]
    show_articles(top_articles)

elif section == "🟢 Last 24h":
    st.header("🟢 Last 24 Hours")
    show_articles(new_24h)

elif section == "🟡 Last 3 Days":
    st.header("🟡 Last 3 Days")
    show_articles(recent_3d)

elif section == "🚨 Company Alerts":
    st.header("🚨 Company Alerts")
    show_articles(alerts)

elif section == "🗺️ State News":
    st.header("🗺️ State News")
    states = defaultdict(list)
    for a in articles:
        states[a["state"]].append(a)
    for state, items in states.items():
        st.subheader(state)
        show_articles(items)