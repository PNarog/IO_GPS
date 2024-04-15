import pandas as pd
import folium


data = pd.read_csv('anomalia_75to100.csv')
map_krakow = folium.Map(location=[50.06143, 19.93658], zoom_start=13)

color_for_anomaly = 'red'
color_for_non_anomaly = 'blue'


for rider_id, group_data in data.groupby('rider_id'):
    
    route = group_data[['szerokosc', 'dlugosc']].values.tolist()
    
    folium.PolyLine(route, color=color_for_non_anomaly, weight=3, opacity=1).add_to(map_krakow)
    
    anomalies = group_data[group_data['anomaly'] == True]
    for _, row in anomalies.iterrows():
        folium.CircleMarker(
            location=[row['szerokosc'], row['dlugosc']],
            radius=5,
            color=color_for_anomaly,
            fill=True,
            fill_color=color_for_anomaly
        ).add_to(map_krakow)

output_map_file = 'krakow_anomalia_75to100.html'
map_krakow.save(output_map_file)

output_map_file