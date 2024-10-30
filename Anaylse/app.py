from flask import Flask, request
from transformers import pipeline
import feedparser
from flask import request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)


pipe = pipeline("text-classification", model="ProsusAI/finbert", device=0)


@app.route("/", methods=["GET"])
def home():
    return "Flask Server is running"


from flask import Flask, request, jsonify
import feedparser

app = Flask(__name__)


@app.route("/analyse", methods=["POST"])
def analyse():
    ticker = request.args.get("ticker", "")
    keywords = request.args.get("keywords", "")
    rss_url = f"https://news.google.com/rss/search?q={ticker}+stock+news+india"
    feed = feedparser.parse(rss_url)

    if not keywords:
        articles = feed.entries
    else:
        keywords = [k.strip().lower() for k in keywords.split(",")]
        articles = [
            entry
            for entry in feed.entries
            if any(keyword in entry.summary.lower() for keyword in keywords)
        ]

    summaries = []
    article_details = []
    score = 0
    total_articles = len(articles)

    for entry in articles:
        # Clean the summary using BeautifulSoup to remove HTML tags
        summary_html = entry.summary
        summary_text = BeautifulSoup(summary_html, "html.parser").get_text()

        # Collect cleaned article details
        details = {
            "title": entry.title,
            "published": entry.published,
            "summary": summary_text,
            "link": entry.link,
        }
        article_details.append(details)
        summaries.append(summary_text)

    # Analyze sentiment using summaries
    sentiments = pipe(summaries)

    for sentiment in sentiments:
        sentiment_score = sentiment["score"]
        if sentiment["label"] == "positive":
            score += sentiment_score
        elif sentiment["label"] == "negative":
            score -= sentiment_score

    final_score = round(score / total_articles, 2) if total_articles > 0 else 0

    if final_score > 0.15:
        sentiment_label = "positive"
    elif final_score < -0.15:
        sentiment_label = "negative"
    else:
        sentiment_label = "neutral"

    return jsonify(
        {
            "score": final_score,
            "sentiment": sentiment_label,
            "total_articles": total_articles,
            "articles": [
                f"Title: {article['title']}\n\n"
                f"Published Date: {article['published']}\n"
                f"Summary: {article['summary']}\n\n"
                f"Link: {article['link']}\n"
                f"--------------------------------------------------------------------"
                for article in article_details
            ],
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
