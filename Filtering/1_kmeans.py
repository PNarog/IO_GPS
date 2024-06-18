import pandas as pd
from sklearn.cluster import KMeans
from geopy.distance import geodesic
import numpy as np

data = pd.read_csv('acc_calculated_data_range_65to69.csv')
data['czas'] = pd.to_datetime(data['czas'], errors='coerce')

# Klasteryzacja przestrzenna
coords = data[['latitude', 'longitude']].values
spatial_kmeans = KMeans(n_clusters=15, random_state=0).fit(coords)
data['spatial_cluster'] = spatial_kmeans.labels_

# Analiza prędkości wewnątrz każdego klastra
for cluster in np.unique(data['spatial_cluster']):
    cluster_data = data[data['spatial_cluster'] == cluster]
    speeds = cluster_data['przyspieszenie_m_s2'].values.reshape(-1, 1)
    speed_kmeans = KMeans(n_clusters=3, random_state=0).fit(speeds)
    centroids = speed_kmeans.cluster_centers_
    distances = speed_kmeans.transform(speeds)
    
    # Próg odległości dla wykrywania anomalii
    threshold = np.percentile(distances, 95)
    
    # Wykrywanie anomalii na podstawie odległości od centroidów
    cluster_data['anomaly'] = distances.min(axis=1) > threshold
    data.loc[cluster_data.index, 'anomaly'] = cluster_data['anomaly']

data.to_csv('anomalia_75to100.csv', index=False)