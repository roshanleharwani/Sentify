import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import yfinance as yf
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Bidirectional
from keras.callbacks import EarlyStopping, ReduceLROnPlateau

company = "NIFTYBEES.NS"

# Define date range
start = dt.datetime(2017, 1, 1)
end = dt.datetime(2024, 10, 1)

# Fetching data using yfinance with additional features
data = yf.download(company, start=start, end=end)
data["HL_PCT"] = (data["High"] - data["Low"]) / data["Low"] * 100
data["PCT_change"] = (data["Close"] - data["Open"]) / data["Open"] * 100
data = data[["Close", "HL_PCT", "PCT_change", "Volume"]]

# Scale data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Prepare training data with extended features
prediction_days = 90
x_train, y_train = [], []

for x in range(prediction_days, len(scaled_data)):
    x_train.append(scaled_data[x - prediction_days : x])
    y_train.append(scaled_data[x, 0])  # predicting only 'Close'

x_train, y_train = np.array(x_train), np.array(y_train)

# Model with increased complexity
model = Sequential()
model.add(
    Bidirectional(
        LSTM(
            units=50,
            return_sequences=True,
            input_shape=(x_train.shape[1], x_train.shape[2]),
        )
    )
)
model.add(Dropout(0.1))
model.add(Bidirectional(LSTM(units=50)))
model.add(Dropout(0.1))
model.add(Dense(units=1))

model.compile(optimizer="adam", loss="mean_absolute_error")  # switching to MAE

# Use early stopping and reduce learning rate
early_stop = EarlyStopping(monitor="loss", patience=10, restore_best_weights=True)
lr_scheduler = ReduceLROnPlateau(monitor="loss", patience=5, factor=0.5, verbose=1)

model.fit(
    x_train, y_train, epochs=50, batch_size=16, callbacks=[early_stop, lr_scheduler]
)

# Testing
test_start = dt.datetime(2024, 10, 2)
test_end = dt.datetime.now()

test_data = yf.download(company, start=test_start, end=test_end)
test_data = test_data[["Close", "High", "Low", "Open", "Volume"]]
test_data["HL_PCT"] = (test_data["High"] - test_data["Low"]) / test_data["Low"] * 100
test_data["PCT_change"] = (
    (test_data["Close"] - test_data["Open"]) / test_data["Open"] * 100
)
test_data = test_data[["Close", "HL_PCT", "PCT_change", "Volume"]]

actual_prices = test_data["Close"].values
total_dataset = pd.concat((data, test_data), axis=0)

model_inputs = total_dataset[
    len(total_dataset) - len(test_data) - prediction_days :
].values
model_inputs = scaler.transform(model_inputs)

# Prepare test data
x_test = []
for x in range(prediction_days, len(model_inputs)):
    x_test.append(model_inputs[x - prediction_days : x])

x_test = np.array(x_test)

# Predictions
predicted_prices = model.predict(x_test)
predicted_prices = scaler.inverse_transform(
    np.hstack(
        (
            predicted_prices,
            np.zeros((predicted_prices.shape[0], scaled_data.shape[1] - 1)),
        )
    )
)[:, 0]

# Predict the next day's price based on the latest input
last_input = model_inputs[-prediction_days:]
last_input = np.expand_dims(last_input, axis=0)
next_day_prediction = model.predict(last_input)
next_day_prediction = scaler.inverse_transform(
    np.hstack(
        (
            next_day_prediction,
            np.zeros((next_day_prediction.shape[0], scaled_data.shape[1] - 1)),
        )
    )
)[0, 0]

print("Predicted price for the next day:", next_day_prediction)

# Plot results
plt.plot(actual_prices, color="black", label="Actual prices")
plt.plot(predicted_prices, color="blue", label="Predicted prices")
plt.title(f"{company} Share Price Prediction")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.show()
