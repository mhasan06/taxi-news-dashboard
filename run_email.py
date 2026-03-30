from scraper import scrape_news_rss_au
from emailer import send_last_24h_articles

print("Running scheduled job...")

articles = scrape_news_rss_au()
send_last_24h_articles(articles)

print("Done sending emails.")