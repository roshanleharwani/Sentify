from transformers import pipeline
import feedparser

# Set up parameters
ticker = "HYUNDAI"
keyword = "IPO"
rss_url = f"https://news.google.com/rss/search?q={ticker}+stock+news+india"

# Initialize sentiment analysis pipeline
pipe = pipeline("text-classification", model="ProsusAI/finbert", device=0)

# Parse the RSS feed
feed = feedparser.parse(rss_url)

# Filter articles containing the keyword
filtered_articles = [
    entry for entry in feed.entries if keyword.lower() in entry.summary.lower()
]

# If there are no relevant articles, handle that case
if not filtered_articles:
    print("No relevant articles found.")
else:
    # Prepare articles for batch processing
    summaries = [entry.summary for entry in filtered_articles]
    sentiments = pipe(summaries)  # Batch process all summaries

    total_articles = len(filtered_articles)
    score = 0

    for entry, sentiment in zip(filtered_articles, sentiments):
        print("Title: ", entry.title)
        print("Published: ", entry.published)
        print(f"Sentiment: {sentiment['label']}, Score: {sentiment['score']:.2f}")
        print("-" * 40)

        # Update score based on sentiment
        if sentiment["label"] == "positive":
            score += sentiment[
                "score"
            ]  # Using actual score for a more nuanced approach
        elif sentiment["label"] == "negative":
            score -= sentiment[
                "score"
            ]  # Using actual score for a more nuanced approach

    # Calculate final sentiment score
    final_score = score / total_articles if total_articles else 0
    sentiment_label = "neutral"

    if final_score > 0.15:
        sentiment_label = "positive"
    elif final_score < -0.15:
        sentiment_label = "negative"

    print("Final Sentiment:", sentiment_label)
