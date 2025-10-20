import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

df = pd.read_csv("ims_dummy_trips.csv")
df["start_time"] = pd.to_datetime(df["start_time"])
df["hour"] = df["start_time"].dt.hour
df["dayofweek"] = df["start_time"].dt.dayofweek

# Group trips by hub/time
demand = df.groupby(["vehicle_type", "hour", "dayofweek"]).size().reset_index(name="trip_count")

enc = OneHotEncoder()
X = enc.fit_transform(demand[["vehicle_type", "hour", "dayofweek"]])
y = demand["trip_count"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation='relu', input_shape=(X.shape[1],)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# ✅ Save model
model.save("demand_predictor_model.keras")
