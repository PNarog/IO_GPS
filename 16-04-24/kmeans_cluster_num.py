import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd

data = pd.read_csv('speed_calculated_data_range_75to100.csv')
coords = data[['szerokosc', 'dlugosc']].values

# Testowanie różnych liczby klastrów
distortions = []
K = range(1, 10)
for k in K:
    kmeanModel = KMeans(n_clusters=k)
    kmeanModel.fit(coords)
    distortions.append(kmeanModel.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(K, distortions, 'bx-')
plt.xlabel('Liczba klastrów')
plt.ylabel('Suma kwadratów odległości')
plt.title('Metoda łokcia')
plt.show()