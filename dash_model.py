from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from tensorflow import keras
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import joblib

# Load trained model
model = keras.models.load_model("demand_predictor_model.h5", compile=False)

# Load data
df = pd.read_csv("ims_big_dummy_trips.csv", parse_dates=["start_time"])

# Prepare hubs data
hubs = df.groupby(["hub_id", "hub_name"]).agg({"lat": "mean", "lng": "mean"}).reset_index()

# --- STATIC CHARTS ---

# 1️⃣ Average rating by vehicle type
avg_rating = df.groupby("vehicle_type")["ride_rating"].mean().reset_index()
fig_bar = px.bar(
    avg_rating,
    x="vehicle_type",
    y="ride_rating",
    color="vehicle_type",
    title="Average Ride Rating by Vehicle Type"
)

# 2️⃣ Trips throughout the day
df["hour"] = df["start_time"].dt.hour
rides_by_hour = df.groupby("hour").size().reset_index(name="trip_count")
fig_line = px.line(
    rides_by_hour,
    x="hour",
    y="trip_count",
    markers=True,
    title="Trips Throughout the Day"
)

# 3️⃣ Duration vs Distance
fig_scatter = px.scatter(
    df,
    x="duration_min",
    y="distance_km",
    color="vehicle_type",
    size="ride_rating",
    title="Relationship Between Duration and Distance"
)

# 4️⃣ Rating distribution
fig_box = px.box(
    df,
    x="vehicle_type",
    y="ride_rating",
    color="vehicle_type",
    title="Ride Rating Distribution by Vehicle Type"
)

# 5️⃣ Trip share pie chart
trips_per_type = df["vehicle_type"].value_counts().reset_index()
trips_per_type.columns = ["vehicle_type", "count"]
fig_pie = px.pie(
    trips_per_type,
    names="vehicle_type",
    values="count",
    title="Trip Share by Vehicle Type"
)

# 6️⃣ Map of trip starts
fig_map = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lng",
    color="vehicle_type",
    size="distance_km",
    hover_name="hub_name",
    mapbox_style="carto-positron",
    zoom=10,
    title="Trip Start Locations by Vehicle Type"
)

# --- DASH APP ---

app = Dash(__name__)
app.layout = html.Div([
    html.H1("E-Scooter Analytics Dashboard", style={"textAlign": "center"}),

    # Grid layout for static charts
    html.Div([
        dcc.Graph(figure=fig_bar, style={"width": "48%", "display": "inline-block"}),
        dcc.Graph(figure=fig_line, style={"width": "48%", "display": "inline-block"}),
    ]),
    html.Div([
        dcc.Graph(figure=fig_scatter, style={"width": "48%", "display": "inline-block"}),
        dcc.Graph(figure=fig_box, style={"width": "48%", "display": "inline-block"}),
    ]),
    html.Div([
        dcc.Graph(figure=fig_pie, style={"width": "48%", "display": "inline-block"}),
        dcc.Graph(figure=fig_map, style={"width": "48%", "display": "inline-block"}),
    ]),

    html.Hr(),

    # Interactive section
    html.H2("Predicted Demand Heatmap", style={"textAlign": "center"}),
    html.Div([
        html.Label("Select Hour of Day:"),
        dcc.Slider(6, 22, 1, value=8, marks={h: str(h) for h in range(6, 23)}, id="hour-slider")
    ], style={"width": "80%", "margin": "auto"}),

    dcc.Graph(id="heatmap")
])

@app.callback(
    Output("heatmap", "figure"),
    Input("hour-slider", "value")
)
def update_map(selected_hour):
    # Use saved encoder if available
    try:
        enc = joblib.load("encoder.joblib")
    except:
        enc = OneHotEncoder()
        # Dummy fit — adjust based on how you trained
        enc.fit([[hub["hub_id"], 12, 0] for _, hub in hubs.iterrows()])

    # Prepare input for prediction
    X_input = []
    for _, hub in hubs.iterrows():
        X_input.append([hub["hub_id"], selected_hour, 0])  # 0 = Monday
    X_input = enc.transform(X_input).toarray()

    # Predict demand
    predictions = model.predict(X_input).flatten()
    hubs["predicted_demand"] = predictions

    # Return updated heatmap
    fig = px.scatter_mapbox(
        hubs, lat="lat", lon="lng", size="predicted_demand", color="predicted_demand",
        hover_name="hub_name", color_continuous_scale="Reds",
        mapbox_style="carto-positron", zoom=10,
        title=f"Predicted Demand — Hour {selected_hour}:00"
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)
