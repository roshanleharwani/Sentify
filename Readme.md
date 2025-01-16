# Sentify: Stock Market Sentiment Analyser

Sentify is an AI-powered platform that provides stock market insights through sentiment analysis and price predictions. It utilizes advanced machine learning models and interactive visualizations to help users better understand market trends and make informed decisions.

## Features

### 1. Stock Sentiment Analysis
- **Stock Ticker Input**: Users can input a stock ticker (e.g., AAPL, TSLA), and Sentify fetches relevant news articles from the past 30 days using Google News.
- **Sentiment Analysis**: Articles are processed using FinBERT, a financial text analysis model hosted on Hugging Face. The sentiment is classified as **Negative**, **Neutral**, or **Positive**.
- **Interactive Visualizations**: Sentiment is displayed with a score on a gauge chart for easy interpretation.
- **Article Sources**: Users can access the news articles used to determine the stock sentiment.

### 2. Stock Price Prediction
- **Stock Ticker and Market Symbol**: Users input the stock ticker and its market symbol (e.g., IRCTC.NS for NSE).
- **Prediction for Up to 1 Year**: Sentify predicts the stock's future price for up to one year, with customizable prediction periods (e.g., 3 months, 6 months, 9 months, 1 year).
- **Interactive Graph**: Predictions are displayed on an interactive Plotly graph, featuring a range slider for user flexibility in selecting prediction periods.

### 3. Market Mood Index
- **Market Indices Insight**: Provides sentiment insights for popular market indices such as Sensex, Nifty50, and Dow Jones.
- **Overall Market Sentiment**: Helps users understand the general market mood and its direction.
