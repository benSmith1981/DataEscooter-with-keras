import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Config
np.random.seed(42)
vehicle_types = ['scooter', 'bike', 'e-bike', 'e-cargo']
hubs = [
    {"hub_id": 1, "hub_name": "Temple Meads", "lat": 51.45, "lng": -2.58},
    {"hub_id": 2, "hub_name": "Clifton", "lat": 51.46, "lng": -2.6},
    {"hub_id": 3, "hub_name": "Bath City Centre", "lat": 51.48, "lng": -2.36},
    {"hub_id": 4, "hub_name": "UWE Campus", "lat": 51.5, "lng": -2.55},
    {"hub_id": 5, "hub_name": "Southmead", "lat": 51.52, "lng": -2.59}
]

rows = []
start_date = datetime(2025, 7, 1)
end_date = datetime(2025, 7, 31)

trip_id = 1
for day in range((end_date - start_date).days + 1):
    for hour in range(6, 23):  # 6am to 10pm
        for hub in hubs:
            # simulate 0–20 trips per hour per hub
            demand = np.random.poisson(lam=random.choice([2, 5, 8, 12]))
            for _ in range(demand):
                vehicle = random.choice(vehicle_types)
                duration = random.randint(5, 25)
                distance = duration * random.uniform(0.05, 0.2)
                rating = random.choice([3, 4, 5])
                rows.append({
                    "trip_id": trip_id,
                    "vehicle_type": vehicle,
                    "start_time": start_date + timedelta(days=day, hours=hour),
                    "hub_id": hub["hub_id"],
                    "hub_name": hub["hub_name"],
                    "lat": hub["lat"] + np.random.uniform(-0.002, 0.002),
                    "lng": hub["lng"] + np.random.uniform(-0.002, 0.002),
                    "duration_min": duration,
                    "distance_km": round(distance, 2),
                    "ride_rating": rating
                })
                trip_id += 1

df = pd.DataFrame(rows)
df.to_csv("ims_big_dummy_trips.csv", index=False)
print("✅ Generated", len(df), "rows of dummy trip data.")
