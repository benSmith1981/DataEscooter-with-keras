from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from tensorflow import keras
from sklearn.preprocessing import OneHotEncoder
import numpy as np

# Load trained model
model = keras.models.load_model("demand_predictor_model.keras", compile=False)

# Load data
df = pd.read_csv("ims_big_dummy_trips.csv", parse_dates=["start_time"])

# Prepare hubs data
hubs = df.groupby(["hub_id", "hub_name"]).agg({"lat": "mean", "lng": "mean"}).reset_index()

# Add hour/dayofweek for prediction
df["hour"] = df["start_time"].dt.hour
df["dayofweek"] = df["start_time"].dt.dayofweek

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Predicted Demand Heatmap"),
    dcc.Slider(6, 22, 1, value=8, marks={h: str(h) for h in range(6, 23)}, id="hour-slider"),
    dcc.Graph(id="heatmap")
])

@app.callback(
    Output("heatmap", "figure"),
    Input("hour-slider", "value")
)
def update_map(selected_hour):
    # Encode inputs
    enc = OneHotEncoder()
    X_input = []
    for _, hub in hubs.iterrows():
        X_input.append([hub["hub_id"], selected_hour, 0])  # 0 = Monday for now
    X_input = enc.fit_transform(X_input).toarray()

    # Predict demand
    predictions = model.predict(X_input).flatten()
    hubs["predicted_demand"] = predictions

    # Map visualization
    fig = px.scatter_mapbox(
        hubs, lat="lat", lon="lng", size="predicted_demand", color="predicted_demand",
        hover_name="hub_name", color_continuous_scale="Reds",
        mapbox_style="carto-positron", zoom=10,
        title=f"Predicted Demand — Hour {selected_hour}:00"
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)
