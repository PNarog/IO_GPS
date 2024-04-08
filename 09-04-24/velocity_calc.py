import pandas as pd
from geopy.distance import geodesic
import numpy as np

try:
    # Wczytanie danych 
    file_path_csv_updated = 'result_ride_range_0to20.csv'  # Aktualizacja ścieżki

    # Odczytanie danych 
    data_for_speed_calculation = pd.read_csv(file_path_csv_updated)

    data_for_speed_calculation['czas'] = pd.to_datetime(data_for_speed_calculation['czas'], errors='coerce')
    data_for_speed_calculation['szerokosc'] = data_for_speed_calculation['szerokosc'].astype(float)
    data_for_speed_calculation['dlugosc'] = data_for_speed_calculation['dlugosc'].astype(float)
    data_for_speed_calculation['wysokosc'] = data_for_speed_calculation['wysokosc'].astype(float)

    data_for_speed_calculation.dropna(subset=['czas', 'szerokosc', 'dlugosc', 'wysokosc'], inplace=True)
    
    # Definiowanie funkcji do obliczenia prędkości
    def calculate_cycling_speed(df):
        speeds = [0]  
        for i in range(1, len(df)):
            prev_point = df.iloc[i - 1]
            current_point = df.iloc[i]
            distance = geodesic((prev_point['szerokosc'], prev_point['dlugosc']),
                                (current_point['szerokosc'], current_point['dlugosc'])).meters
            time_diff = (current_point['czas'] - prev_point['czas']).total_seconds()
            speed = distance / time_diff if time_diff > 0 else 0
            speeds.append(speed)
        df['predkosc_m_s'] = speeds
        return df

    data_with_speed_updated = calculate_cycling_speed(data_for_speed_calculation)
    
    # Zapisanie DataFrame 
    output_file_path = 'output/speed_calculated_data.csv' 
    data_with_speed_updated.to_csv(output_file_path, index=False)
    print(f"Dane zostały zapisane do pliku: {output_file_path}")
    
except Exception as e:
    print(f"Wystąpił błąd: {e}")