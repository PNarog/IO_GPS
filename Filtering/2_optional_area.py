import pandas as pd
from geopy.distance import geodesic
import numpy as np

# Load the data
data = pd.read_csv('anomalia_75to100.csv')

# Select only rows where 'anomaly' is True
anomalies = data[data['anomaly'] == True]

# Prepare an empty list to store indices of anomalies to keep
indices_to_keep = []

# Compare each anomaly against all others
for i in range(len(anomalies)):
    current = anomalies.iloc[i]
    current_coords = (current['latitude'], current['longitude'])
    count_nearby = 0  # Counter for nearby anomalies

    for j in range(len(anomalies)):
        if i != j:
            comparison = anomalies.iloc[j]
            comparison_coords = (comparison['latitude'], comparison['longitude'])
            # Calculate the distance
            if geodesic(current_coords, comparison_coords).meters <= 10:
                count_nearby += 1

    # Check if there are at least two other anomalies within 10 meters
    if count_nearby >= 2:
        indices_to_keep.append(current.name)

# Update 'anomaly' column in the original dataset
data['anomaly'] = data.index.isin(indices_to_keep)

# Save the updated dataset
data.to_csv('updated_anomalies.csv', index=False)