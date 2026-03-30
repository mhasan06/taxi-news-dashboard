# test_email.py
from emailer import send_company_alerts

dummy_articles = [
    {
        "title": "Uber faces new regulations in Sydney",
        "link": "https://example.com",
        "company": "Uber",
        "summary": "Uber faces new government rules.",
        "impact": "Negative"
    }
]

send_company_alerts(dummy_articles, "mhasan06@gmail.com")