from geopy.distance import geodesic
from datetime import datetime
import gpxpy
import pandas as pd
import folium


def read_gpx(file_path):
    data = []

    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:

            for segment in track.segments:
                for point in segment.points:
                    time = point.time
                    coordinates = (point.latitude, point.longitude)
                    height = point.elevation
                    data.append({"czas": time, "wspolrzedne": coordinates, "wysokosc": height})

    calculate_speed(data, output_file_path)


def calculate_speed(data, output_file):
    speed_data = []

    for i in range(1, len(data)):
        start_point = data[i - 1]
        end_point = data[i]

        start_time = start_point["czas"]
        end_time = end_point["czas"]

        distance = geodesic(start_point["wspolrzedne"], end_point["wspolrzedne"]).meters
        time_difference = (end_time - start_time).total_seconds()  # Time difference in seconds

        speed = distance / time_difference
        speed_data.append({"Start Time": start_time, "End Time": end_time, "Speed (m/s)": speed,
                           "End Latitude": end_point["wspolrzedne"][0], "End Longitude": end_point["wspolrzedne"][1]})

    df = pd.DataFrame(speed_data)
    df.to_csv(output_file, index=False)
    print(f"Dane zostały zapisane do pliku Excel: {output_file}")

    krakow_map = folium.Map(location=[50.0647, 19.9450], zoom_start=13)

    for index, row in df.iterrows():
        folium.Marker([row['End Latitude'], row['End Longitude']],
                      popup=f"End Time: {row['End Time']}, Speed: {row['Speed (m/s)']} m/s").add_to(krakow_map)

    krakow_map.save("krakow_map.html")
    print("Mapa została zapisana do pliku krakow_map.html")


gpx_file_path = 'STRAVAnowa/MALE/RANGE0to19/ride.10954734.gpx'
output_file_path = 'results/ride10954734.csv'
read_gpx(gpx_file_path)



