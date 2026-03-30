# ai_utils.py
from openai import OpenAI
import json

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def analyze_article(title):
    prompt = f"""
    You are analysing news for the Australian taxi industry.

    Article title: "{title}"

    1. Give a short 1-2 line summary.
    2. Classify impact on taxi industry as:
       Positive, Negative, or Neutral.

    Respond in JSON:
    {{
        "summary": "...",
        "impact": "Positive/Negative/Neutral"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        return data["summary"], data["impact"]

    except:
        return "Summary unavailable", "Neutral"