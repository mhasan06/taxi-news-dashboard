from transformers import pipeline

# Load once (may take time first run)
classifier = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def get_sentiment(text):
    try:
        result = classifier(text[:512])[0]
        label = result["label"]
        score = result["score"]

        if label == "positive":
            return score
        elif label == "negative":
            return -score
        else:
            return 0
    except:
        return 0