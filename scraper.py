# scraper.py
import feedparser
import requests
from datetime import datetime

# -----------------------------
# RSS SOURCES
# -----------------------------
RSS_FEEDS = {
    "Google News": "https://news.google.com/rss/search?q=uber+OR+taxi+OR+rideshare&hl=en-AU&gl=AU&ceid=AU:en",
    "ABC News": "https://www.abc.net.au/news/feed/51120/rss.xml",
    "Guardian AU": "https://www.theguardian.com/au/rss",
    "SMH": "https://www.smh.com.au/rss/feed.xml",
    "The Age": "https://www.theage.com.au/rss/feed.xml"
}

# -----------------------------
# KEYWORDS
# -----------------------------
KEYWORDS = [
    "uber", "taxi", "rideshare", "cab", "13cabs", "silver service",
    "a2b", "lyft", "didi", "grab", "bolt", "taxify",
    # NEW: payment-related terms included
    "surcharge", "taxi fee", "taxi fees", "taxi payment", "card charge", "transaction fee"
]

# NEW: Payment keywords
PAYMENT_KEYWORDS = [
    "surcharge", "surcharges", "fee", "fees",
    "payment fee", "card fee", "credit card fee", "debit card fee",
    "transaction fee", "processing fee", "merchant fee",
    "service fee", "booking fee", "extra charge",
    "fare increase", "fare change", "pricing change"
]

COMPANY_KEYWORDS = {
    "A2B": ["a2b", "a2b australia"],
    "13cabs": ["13cabs", "13 cabs"],
    "Silver Service": ["silver service"],
    "Lyft": ["lyft"],
    "Didi": ["didi"],
    "Grab": ["grab"],
    "Bolt": ["bolt"],
    "Taxify": ["taxify"],
    "GM Cabs": ["gm cabs", "gm taxis"],
}

STATE_KEYWORDS = {
    "NSW": "New South Wales", "Sydney": "New South Wales",
    "VIC": "Victoria", "Melbourne": "Victoria",
    "QLD": "Queensland", "Brisbane": "Queensland",
    "WA": "Western Australia", "Perth": "Western Australia",
    "SA": "South Australia", "Adelaide": "South Australia",
    "TAS": "Tasmania", "Hobart": "Tasmania",
    "NT": "Northern Territory", "Darwin": "Northern Territory",
    "ACT": "Australian Capital Territory", "Canberra": "Australian Capital Territory"
}

# -----------------------------
# FREE AI (RULE-BASED)
# -----------------------------
def analyze_article(title):
    title_lc = title.lower()

    # Detect payment-related
    is_payment_related = any(word in title_lc for word in PAYMENT_KEYWORDS)

    negative_words = [
        "surge", "lawsuit", "ban", "fine",
        "crackdown", "shortage", "strike", "protest"
    ]

    positive_words = [
        "growth", "expand", "launch",
        "profit", "partnership", "upgrade"
    ]

    # Smarter logic for payment impact
    if is_payment_related:
        if any(w in title_lc for w in ["cut", "reduce", "scrap", "remove", "drop"]):
            impact = "Positive"
        elif any(w in title_lc for w in ["increase", "rise", "higher"]):
            impact = "Negative"
        else:
            impact = "Negative"  # default = revenue risk
    elif any(word in title_lc for word in negative_words):
        impact = "Negative"
    elif any(word in title_lc for word in positive_words):
        impact = "Positive"
    else:
        impact = "Neutral"

    summary = title.strip()

    return summary, impact, is_payment_related

# -----------------------------
# HELPERS
# -----------------------------
def is_relevant(title):
    title_lc = title.lower()
    return any(k in title_lc for k in KEYWORDS)

def get_state(title):
    title_lc = title.lower()
    for keyword, state in STATE_KEYWORDS.items():
        if keyword.lower() in title_lc:
            return state
    return "National"

def detect_company(title):
    title_lc = title.lower()
    for company, keywords in COMPANY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in title_lc:
                return company
    return None

def fetch_feed(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, timeout=8, headers=headers)
    return feedparser.parse(response.content)

# -----------------------------
# SCRAPER
# -----------------------------
def scrape_news_rss_au():
    news = []

    for source, url in RSS_FEEDS.items():
        try:
            feed = fetch_feed(url)
        except:
            continue

        if not feed or not feed.entries:
            continue

        for entry in feed.entries[:20]:
            title = entry.get("title", "")
            if not is_relevant(title):
                continue

            link = entry.get("link", "")

            if entry.get("published_parsed"):
                published_dt = datetime(*entry.published_parsed[:6])
            elif entry.get("updated_parsed"):
                published_dt = datetime(*entry.updated_parsed[:6])
            else:
                published_dt = datetime.utcnow()

            summary, impact, is_payment_related = analyze_article(title)

            news.append({
                "title": title,
                "link": link,
                "published": published_dt,
                "state": get_state(title),
                "source": source,
                "company": detect_company(title),
                "summary": summary,
                "impact": impact,
                "payment_related": is_payment_related  # NEW FIELD
            })

    return news
