from geopy.distance import geodesic
import gpxpy
import pandas as pd
import folium
import numpy as np

def read_gpx(file_path, output_file_path, case):
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

    if case == 1:
        calculate_speed_and_direction(data, output_file_path)
    else:
        calculate_speed(data, output_file_path)

def calculate_speed(data, output_file):
    speed_data = []

    for i in range(1, len(data)):
        start_point = data[i - 1]
        end_point = data[i]

        start_time = start_point["czas"]
        end_time = end_point["czas"]

        distance = geodesic(start_point["wspolrzedne"], end_point["wspolrzedne"]).meters
        time_difference = (end_time - start_time).total_seconds()

        speed = distance / time_difference if time_difference > 0 else 0
        speed_data.append({"Start Time": start_time, "End Time": end_time, "Speed (m/s)": speed,
                           "End Latitude": end_point["wspolrzedne"][0], "End Longitude": end_point["wspolrzedne"][1]})

    df = pd.DataFrame(speed_data)

    # Normalizacja prędkości
    max_speed = df["Speed (m/s)"].max()
    min_speed = df["Speed (m/s)"].min()
    df["Normalized Speed"] = (df["Speed (m/s)"] - min_speed) / (max_speed - min_speed)

    # Zapis do pliku CSV
    df.to_csv(output_file, index=False)
    print(f"Dane zostały zapisane do pliku: {output_file}")

    draw_map(df)

def draw_map(df):
    krakow_map = folium.Map(location=[50.0647, 19.9450], zoom_start=13)

    for index, row in df.iterrows():
        color = get_color(row['Normalized Speed'])
        folium.CircleMarker([row['End Latitude'], row['End Longitude']],
                            radius=5,
                            color=color,
                            fill=True,
                            fill_color=color,
                            popup=f"End Time: {row['End Time']}, Speed: {row['Speed (m/s)']} m/s").add_to(krakow_map)

    krakow_map.save("krakow_map_heatmap.html")


def get_color(normalized_speed):
    """Funkcja do określania koloru na podstawie znormalizowanej prędkości."""
    if normalized_speed < 0.2:
        return '#0000FF'  # niebieski
    elif normalized_speed < 0.4:
        return '#00FF00'  # jasnozielony
    elif normalized_speed < 0.6:
        return '#FFFF00'  # żółty
    elif normalized_speed < 0.8:
        return '#FFA500'  # pomarańczowy
    else:
        return '#FF0000'  # czerwony

def calculate_speed_and_direction(data, output_file):
    speed_data = []

    for i in range(1, len(data)):
        start_point = data[i - 1]
        end_point = data[i]

        start_time = start_point["czas"]
        end_time = end_point["czas"]

        distance = geodesic(start_point["wspolrzedne"], end_point["wspolrzedne"]).meters
        time_difference = (end_time - start_time).total_seconds()

        speed = distance / time_difference if time_difference > 0 else 0
        direction = np.arctan2(
            end_point["wspolrzedne"][1] - start_point["wspolrzedne"][1],
            end_point["wspolrzedne"][0] - start_point["wspolrzedne"][0]
        ) * (180 / np.pi)  # Przeliczenie na stopnie

        speed_data.append({
            "Start Time": start_time, "End Time": end_time, "Speed (m/s)": speed, "Direction": direction,
            "Start Latitude": start_point["wspolrzedne"][0], "Start Longitude": start_point["wspolrzedne"][1],
            "End Latitude": end_point["wspolrzedne"][0], "End Longitude": end_point["wspolrzedne"][1]
        })

    df = pd.DataFrame(speed_data)

    # Normalizacja prędkości
    max_speed = df["Speed (m/s)"].max()
    min_speed = df["Speed (m/s)"].min()
    df["Normalized Speed"] = (df["Speed (m/s)"] - min_speed) / (max_speed - min_speed)

    # Zapis do pliku CSV
    df.to_csv(output_file, index=False)
    print(f"Dane zostały zapisane do pliku: {output_file}")

    draw_map_with_directions(df)

def draw_map_with_directions(df):
    krakow_map = folium.Map(location=[50.0647, 19.9450], zoom_start=13)

    # Określenie ilości strzałek na trasie w zależności od jej długości.
    arrow_length = max(len(df) // 20, 1)  # Co najmniej jedna strzałka, ale więcej dla dłuższych tras

    for index in range(len(df)):
        if index % arrow_length == 0:  # Dodajemy strzałki w równych odstępach
            row = df.iloc[index]
            color = get_color(row['Normalized Speed'])
            folium.PolyLine([(row['Start Latitude'], row['Start Longitude']), (row['End Latitude'], row['End Longitude'])],
                            color=color, weight=2.5, opacity=1).add_to(krakow_map)
            

            add_arrow(krakow_map, row['Start Latitude'], row['Start Longitude'], row['End Latitude'], row['End Longitude'], color)

    krakow_map.save("krakow_map_orientation.html")

def add_arrow(map_obj, start_lat, start_lon, end_lat, end_lon, color):
    """Funkcja do dodawania strzałki wskazującej kierunek na mapie."""

    angle = np.arctan2(end_lon - start_lon, end_lat - start_lat) * 180 / np.pi

    folium.RegularPolygonMarker(location=[end_lat, end_lon],
                                fill_color=color,
                                number_of_sides=3,
                                radius=6,
                                rotation=angle,
                                color=color).add_to(map_obj)
    

gpx_file_path = 'STRAVAnowa/MALE/RANGE0to19/ride.10954734.gpx'
output_file_path = 'results/ride10954734.csv'
read_gpx(gpx_file_path, output_file_path, case=0)