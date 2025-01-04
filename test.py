import yfinance as yf
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy import stats

# Fetch stock data from Yahoo Finance (Example: Apple stock, 'AAPL')
stock_symbol = "AAPL"  # Change to the desired stock symbol
start_date = "2023-01-01"  # Start date for data collection
end_date = "2024-01-01"  # End date for data collection

# Download historical data using yfinance
data = yf.download(stock_symbol, start=start_date, end=end_date)

# Extract the 'Adj Close' prices for analysis
data = data[["Adj Close"]].reset_index()

# Check if 'Adj Close' is present
print("Columns available in data:", data.columns)

# 1. General Overview Graph
fig1 = go.Figure()
fig1.add_trace(
    go.Scatter(x=data["Date"], y=data["Adj Close"], mode="lines", name="Stock Price")
)
fig1.update_layout(
    title=f"{stock_symbol} Stock Price General Overview",
    xaxis_title="Time",
    yaxis_title="Price",
)

# 2. Derivative Graph (Rate of Change of Stock Prices)
# Ensure 'Adj Close' is present and calculate the derivative
if "Adj Close" in data.columns:
    data["Derivative"] = np.diff(
        data["Adj Close"], prepend=data["Adj Close"].iloc[0]
    )  # Use iloc[0] for first value
else:
    print("Column 'Adj Close' not found in data.")

fig2 = go.Figure()
fig2.add_trace(
    go.Scatter(
        x=data["Date"],
        y=data["Derivative"],
        mode="lines",
        name="Derivative of Stock Price",
    )
)
fig2.update_layout(
    title="Derivative of Stock Price (Rate of Change)",
    xaxis_title="Time",
    yaxis_title="Derivative",
)

# 3. Probability of Crash Graph (Using a simple logistic regression model as an example)
# A simple crash prediction model using price volatility and derivative (Rate of change)
# For illustration purposes, we'll create a binary crash prediction based on the derivative.

# Define a threshold for volatility (e.g., if derivative > some threshold, consider it a "crash-like" event)
threshold = 1.5
data["Crash_Likelihood"] = np.where(np.abs(data["Derivative"]) > threshold, 1, 0)

# Calculate probability of crash based on a simple model
# Logistic regression or other models could be used, here we use a simple linear model for simplicity
slope, intercept, r_value, p_value, std_err = stats.linregress(
    np.arange(len(data)), data["Crash_Likelihood"]
)
data["Crash_Probability"] = 1 / (
    1 + np.exp(-(slope * np.arange(len(data)) + intercept))
)

fig3 = go.Figure()
fig3.add_trace(
    go.Scatter(
        x=data["Date"],
        y=data["Crash_Probability"],
        mode="lines",
        name="Crash Probability",
    )
)
fig3.update_layout(
    title="Crash Probability Prediction", xaxis_title="Time", yaxis_title="Probability"
)

# Show the graphs
fig1.show()
fig2.show()
fig3.show()
