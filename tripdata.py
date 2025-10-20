import pandas as pd
import matplotlib.pyplot as plt

# Read in the dataset
df = pd.read_csv("ims_dummy_trips.csv")

# Display the first few rows
print(df.head())

#This shows the average rating 
# for a ride from the ride_rating column

print(df["battery_end"].mean()) #mean battery at end
print(df["ride_rating"].mean()) #mean overall ratings

#Mean rating of each vehicle type...
print(df.groupby('vehicle_type')['ride_rating'].mean())
vehicleType_rating = df.groupby('vehicle_type')['ride_rating'].mean()

plt.bar(vehicleType_rating.index,vehicleType_rating.values)
plt.title("Average Ride Rating by Vehicle Type")
plt.xlabel("Vehicle Type")
plt.ylabel("Average Rating")
plt.show()

