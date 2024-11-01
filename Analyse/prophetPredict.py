from prophet import Prophet
from datetime import datetime
import yfinance as yf
import plotly.graph_objs as go
from plotly.offline import plot

# Step 1: Get the data
start = datetime(2020, 1, 1)
end = datetime.now()
company = "HDFCBANK.NS"
data = yf.download(company, start=start, end=end)
data = data.reset_index()
data = data[["Date", "Close"]]
data.columns = ["ds", "y"]

data["ds"] = data["ds"].dt.tz_localize(None)

# Step 2: Train the Prophet model
model = Prophet(daily_seasonality=True)
model.fit(data)

# Step 3: Make predictions
future_dates = model.make_future_dataframe(periods=365)
predictions = model.predict(future_dates)

# Step 4: Create an interactive Plotly figure
fig = go.Figure()

# Add actual data as scatter plot
fig.add_trace(
    go.Scatter(
        x=data["ds"],
        y=data["y"],
        mode="markers",
        name="Actual Prices",
        marker=dict(color="black"),
    )
)

# Add predicted data as line plot
fig.add_trace(
    go.Scatter(
        x=predictions["ds"],
        y=predictions["yhat"],
        mode="lines",
        name="Predicted Prices",
        line=dict(color="blue"),
    )
)

# Add shaded area for uncertainty (confidence interval)
fig.add_trace(
    go.Scatter(
        x=predictions["ds"].tolist() + predictions["ds"][::-1].tolist(),
        y=predictions["yhat_upper"].tolist() + predictions["yhat_lower"][::-1].tolist(),
        fill="toself",
        fillcolor="rgba(100,200,230,0.4)",  # Light blue color for the fill
        line=dict(color="rgba(255,255,255,0)"),
        hoverinfo="skip",
        showlegend=True,
        name="Uncertainty Interval",
    )
)

# Customize layout
fig.update_layout(
    title="TSLA Stock Price Prediction",
    xaxis_title="Date",
    yaxis_title="Price",
    legend_title="Legend",
)

# Customize layout with range slider
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


fig.show()
# Step 5: Export the figure to HTML
graph_html = plot(fig, output_type="div")  # Returns HTML <div> of the plot
