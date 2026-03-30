from datetime import datetime
from nlp import get_sentiment

def time_weight(published_time):
    try:
        delta = datetime.now() - datetime.fromisoformat(published_time)
        hours = delta.total_seconds() / 3600
        return max(0.1, 1 / (1 + hours))
    except:
        return 0.5

def compute_signal(news, market):
    scores = []

    for item in news:
        sentiment = get_sentiment(item["title"])
        weight = time_weight(item["time"])
        scores.append(sentiment * weight)

    if not scores:
        return "HOLD ⚖️", 0

    news_score = sum(scores) / len(scores)

    momentum = market["momentum"]
    volume = market["volume_spike"]

    combined = (news_score * 0.5) + (momentum * 0.3) + (volume * 0.2)
    confidence = min(1.0, abs(combined) * 2)

    if combined > 0.05:
        return "BUY 📈", confidence
    elif combined < -0.05:
        return "SELL 📉", confidence
    else:
        return "HOLD ⚖️", confidence