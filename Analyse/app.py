from flask import Flask, request
from transformers import pipeline
import feedparser
from flask import request, jsonify
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import plotly.graph_objs as go
from plotly.offline import plot
from prophet import Prophet
import yfinance as yf

app = Flask(__name__)


pipe = pipeline("text-classification", model="ProsusAI/finbert", device=0)


@app.route("/", methods=["GET"])
def home():
    return "Flask Server is running"


@app.route("/analyse", methods=["POST"])
def analyse():
    ticker = request.args.get("ticker", "")
    keywords = request.args.get("keywords", "")
    country = request.args.get("country", "india")
    rss_url = f"https://news.google.com/rss/search?q={ticker}+stock+news+{country}"
    feed = feedparser.parse(rss_url)

    # Calculate the date for the two-month constraint
    two_months_ago = datetime.now() - timedelta(days=30)

    # Filter articles based on the keyword and two-month constraint
    if not keywords:
        articles = [
            entry
            for entry in feed.entries
            if datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
            > two_months_ago
        ]
    else:
        keywords = [k.strip().lower() for k in keywords.split(",")]
        articles = [
            entry
            for entry in feed.entries
            if any(keyword in entry.summary.lower() for keyword in keywords)
            and datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
            > two_months_ago
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

    if final_score > 0.05:
        sentiment_label = "positive"
    elif final_score < -0.05:
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


@app.route("/predict", methods=["POST"])
def predict():
    company = request.args.get("ticker")
    date = request.args.get("date")
    period = int(request.args.get("period", 1))
    print(company, date, period)
    start = datetime.strptime(date, "%Y-%m-%d")
    end = datetime.now()
    data = yf.download(company, start=start, end=end)
    data = data.reset_index()
    data = data[["Date", "Close"]]
    data.columns = ["ds", "y"]
    data["ds"] = data["ds"].dt.tz_localize(None)
    model = Prophet(daily_seasonality=True)
    model.fit(data)
    future_dates = model.make_future_dataframe(periods=period * 91)
    predictions = model.predict(future_dates)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data["ds"],
            y=data["y"],
            mode="markers",
            name="Actual Prices",
            marker=dict(color="black"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=predictions["ds"],
            y=predictions["yhat"],
            mode="lines",
            name="Predicted Prices",
            line=dict(color="blue"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=predictions["ds"].tolist() + predictions["ds"][::-1].tolist(),
            y=predictions["yhat_upper"].tolist()
            + predictions["yhat_lower"][::-1].tolist(),
            fill="toself",
            fillcolor="rgba(100,200,230,0.4)",  # Light blue color for the fill
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            showlegend=True,
            name="Uncertainty Interval",
        )
    )
    fig.update_layout(
        title="TSLA Stock Price Prediction",
        xaxis_title="Date",
        yaxis_title="Price",
        legend_title="Legend",
    )
    fig.update_layout(
        title=f"{company} Stock Price Prediction",
        xaxis_title="Date",
        yaxis_title="Price",
        legend_title="Legend",
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        ),
    )
    return plot(fig, output_type="div")


if __name__ == "__main__":
    app.run(debug=True)
