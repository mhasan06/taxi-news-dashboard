import streamlit as st
from scraper import scrape_news_rss_au
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh
# Last refresh time
st.caption(f"🕒 Last updated: {datetime.now().strftime('%d %b %Y %I:%M %p')}")
st.markdown("---")  # horizontal line
st.caption("Developed by Mohammad Hasan")

# Auto refresh every 10 minutes
st_autorefresh(interval=600000, key="refresh")

st.set_page_config(page_title="Taxi News AU", layout="wide")
st.title("🚖 Taxi / Rideshare News Dashboard")

# Fetch data
articles = scrape_news_rss_au()
now = datetime.utcnow()

def in_last_24h(a):
    return (now - a["published"]) < timedelta(hours=24)

new_24h = [a for a in articles if in_last_24h(a)]

st.header("🟢 Last 24 Hours News")

if not new_24h:
    st.write("No recent news found.")
else:
    for item in new_24h:
        st.subheader(item["title"])
        st.write(f"📰 {item['source']} | 📅 {item['published']}")
        st.write(f"🧠 {item['summary']}")
        st.write(f"📊 Impact: {item['impact']}")
        if item["company"]:
            st.warning(f"🏢 Company: {item['company']}")
        st.markdown(f"[Read more]({item['link']})")
        st.markdown("---")