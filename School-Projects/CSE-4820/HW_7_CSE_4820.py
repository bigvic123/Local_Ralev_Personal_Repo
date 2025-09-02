import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import yfinance as yf

np.random.seed(42)
tf.random.set_seed(42)

# stock data
start_date = "2016-01-01"
end_date = "2021-12-01"
data = yf.download("TSLA", start=start_date, end=end_date)
close_prices = data['Close'].values

# Normalizing data
min_val = np.min(close_prices)
max_val = np.max(close_prices)
scaled_data = (close_prices - min_val) / (max_val - min_val)

training_data_len = len(scaled_data) - 252  
train_data = scaled_data[:training_data_len]
test_data = scaled_data[training_data_len - 60:]  

# Creating datasets
def create_dataset(data, window_size=60):
    X, y = [], []
    for i in range(window_size, len(data)):
        X.append(data[i-window_size:i])
        y.append(data[i])
    return np.array(X), np.array(y)

X_train, y_train = create_dataset(train_data)
X_test, y_test = create_dataset(test_data)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Build model
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
    tf.keras.layers.LSTM(50, return_sequences=False),
    tf.keras.layers.Dense(25),
    tf.keras.layers.Dense(1)
])
model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(X_train, y_train, batch_size=1, epochs=1)

# Predictions
predictions = model.predict(X_test)
predictions = predictions * (max_val - min_val) + min_val  # Reverse normalization
y_test = y_test * (max_val - min_val) + min_val  # Reverse normalization

rmse = np.sqrt(np.mean((predictions - y_test) ** 2))
print(f"RMSE: {rmse}")

# Plot prediction curve
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = predictions

plt.figure(figsize=(16, 8))
plt.title('Model Predictions')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price USD ($)', fontsize=18)
plt.plot(train['Close'], label='Train Data')
plt.plot(valid[['Close']], label='Test Data')
plt.plot(valid[['Predictions']], label='Predictions')
plt.legend()
plt.show()
