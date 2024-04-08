import pandas as pd
import folium
from geopy.distance import geodesic
import numpy as np
from matplotlib import pyplot as plt

file_path_visualization = 'output/speed_calculated_data.csv'

# Wczytanie danych do DataFrame
data_for_visualization_folium = pd.read_csv(file_path_visualization)


data_for_visualization_folium['czas'] = pd.to_datetime(data_for_visualization_folium['czas'])


rider_ids = data_for_visualization_folium['rider_id'].unique()
colors = plt.cm.rainbow(np.linspace(0, 1, len(rider_ids)))
color_dict = dict(zip(rider_ids, colors))


krakow_map_corrected = folium.Map(location=[50.06143, 19.93658], zoom_start=13)


def convert_color_to_hex_corrected(color):
    return '#'+(''.join([('%0.2X' % int(c*255)) for c in color[:3]]))

# Dodanie tras każdego rowerzysty do mapy, korzystając z zaktualizowanych danych
for rider_id, group_data in data_for_visualization_folium.groupby('rider_id'):
    points = group_data[['szerokosc', 'dlugosc']].values.tolist()
    color_hex = convert_color_to_hex_corrected(color_dict[rider_id])
    folium.PolyLine(points, color=color_hex, weight=2.5, opacity=1).add_to(krakow_map_corrected)

# Zapisanie mapy
krakow_map_corrected.save('output/krakow_cycling_map_corrected.html')

'output/krakow_cycling_map_corrected.html'