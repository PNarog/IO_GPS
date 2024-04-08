import pandas as pd
from geopy.distance import geodesic
import numpy as np
from matplotlib import pyplot as plt

file_path_visualization = 'output/speed_calculated_data.csv'

# Wczytanie danych 
data_for_visualization = pd.read_csv(file_path_visualization)

data_for_visualization['czas'] = pd.to_datetime(data_for_visualization['czas'])

rider_ids = data_for_visualization['rider_id'].unique()
colors = plt.cm.rainbow(np.linspace(0, 1, len(rider_ids)))
color_dict = dict(zip(rider_ids, colors))

plt.figure(figsize=(15, 10))

# Rysowanie tras każdego rowerzysty różnym kolorem
for rider_id, group_data in data_for_visualization.groupby('rider_id'):
    plt.plot(group_data['dlugosc'], group_data['szerokosc'], label=rider_id, color=color_dict[rider_id])

plt.title('Trasy rowerzystów')
plt.xlabel('Długość geograficzna')
plt.ylabel('Szerokość geograficzna')

plt.legend()

plt.savefig('output/visualization_matplotlib.png')

plt.show()