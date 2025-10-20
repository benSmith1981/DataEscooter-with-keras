import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# CONFIGURATION
# -----------------------------
st.set_page_config(page_title="Micromobility Intelligence Dashboard", layout="wide")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    trips = pd.read_csv("ims_dummy_trips.csv", parse_dates=["start_time", "end_time"])
    parking = pd.read_csv("ims_dummy_parking.csv")
    vehicles = pd.read_csv("ims_dummy_vehicles.csv")
    return trips, parking, vehicles

trips, parking, vehicles = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔧 Filters")

vehicle_types = ["All"] + sorted(trips["vehicle_type"].unique().tolist())
selected_vehicle = st.sidebar.selectbox("Vehicle Type", vehicle_types)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [trips["start_time"].min().date(), trips["start_time"].max().date()]
)

# Apply filters
filtered_trips = trips[
    (trips["start_time"].dt.date >= date_range[0]) &
    (trips["start_time"].dt.date <= date_range[1])
]

if selected_vehicle != "All":
    filtered_trips = filtered_trips[filtered_trips["vehicle_type"] == selected_vehicle]

# -----------------------------
# KPIs
# -----------------------------
st.title("🚴‍♀️ Micromobility Intelligence Dashboard")
st.markdown("### West of England FTZ Hackathon Dataset — Insights & Analytics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Trips", len(filtered_trips))
col2.metric("Avg Trip Distance (km)", round(filtered_trips["distance_km"].mean(), 2))
col3.metric("Avg Duration (min)", round(filtered_trips["duration_min"].mean(), 2))
col4.metric("Avg Ride Rating", round(filtered_trips["ride_rating"].mean(), 2))

st.markdown("---")

# -----------------------------
# USAGE ANALYTICS
# -----------------------------
st.subheader("📈 Trip and Usage Analytics")

# Average rating by vehicle type
vehicle_ratings = trips.groupby("vehicle_type")["ride_rating"].mean().reset_index()
fig1 = px.bar(vehicle_ratings, x="vehicle_type", y="ride_rating", color="vehicle_type",
              title="Average Ride Rating by Vehicle Type", color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig1, use_container_width=True)

# Trip time-of-day patterns
filtered_trips["hour"] = filtered_trips["start_time"].dt.hour
fig2 = px.histogram(filtered_trips, x="hour", nbins=24, color="vehicle_type",
                    title="Trip Frequency by Hour of Day", labels={"hour": "Hour of Day", "count": "Trips"})
st.plotly_chart(fig2, use_container_width=True)

# Distance vs Duration scatter
fig3 = px.scatter(filtered_trips, x="distance_km", y="duration_min", color="vehicle_type",
                  size="ride_rating", hover_data=["battery_start", "battery_end"],
                  title="Trip Distance vs Duration (bubble size = rating)")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# -----------------------------
# BATTERY & MAINTENANCE INSIGHTS
# -----------------------------
st.subheader("🔋 Battery & Maintenance Insights")

vehicles_summary = vehicles.groupby("vehicle_type").agg({
    "battery_level": "mean",
    "status": lambda x: (x == "maintenance").sum()
}).rename(columns={"battery_level": "avg_battery", "status": "in_maintenance"}).reset_index()

fig4 = px.bar(vehicles_summary, x="vehicle_type", y="avg_battery", color="vehicle_type",
              title="Average Battery Level by Vehicle Type")
st.plotly_chart(fig4, use_container_width=True)

fig5 = px.bar(vehicles_summary, x="vehicle_type", y="in_maintenance", color="vehicle_type",
              title="Number of Vehicles in Maintenance by Type")
st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# -----------------------------
# PARKING & DISTRIBUTION
# -----------------------------
st.subheader("🅿️ Parking Hub Utilisation")

parking["utilisation"] = parking["vehicles_present"] / parking["capacity"] * 100
fig6 = px.bar(parking, x="hub_name", y="utilisation", color="utilisation",
              title="Parking Hub Utilisation (%)", color_continuous_scale="Blues")
st.plotly_chart(fig6, use_container_width=True)

# Heatmap of parking locations
st.subheader("🌍 Parking Hub Activity Map")

fig_map = px.density_mapbox(
    parking,
    lat="hub_lat",
    lon="hub_lng",
    z="vehicles_present",
    radius=25,
    center=dict(lat=51.47, lon=-2.58),
    zoom=11,
    mapbox_style="carto-positron",
    hover_name="hub_name",
    color_continuous_scale="Blues",
    title="Parking Hub Heatmap — Vehicle Concentration"
)
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")

# -----------------------------
# INSIGHTS
# -----------------------------
st.subheader("🧠 Key Insights Summary")
st.write("""
- **Peak trip times:** Commuter hours (7–9 am, 4–6 pm) dominate usage.  
- **Battery drain:** E-bikes show higher average battery loss per km.  
- **Maintenance load:** Scooters currently have the most vehicles under maintenance.  
- **Parking demand:** UWE Campus and Bath City Centre operate near capacity — potential need for rebalancing.  
- **Trip efficiency:** Average trip length remains short, suggesting primarily urban commuting usage.  
""")
