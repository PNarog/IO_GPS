import pandas as pd
import matplotlib.pyplot as plt



data = pd.read_csv('anomalia_0to20_18c.csv')

fig, ax = plt.subplots()

unique_clusters = data['spatial_cluster'].unique()
cmap = plt.cm.get_cmap('viridis', len(unique_clusters))

for i, cluster in enumerate(unique_clusters):

    cluster_data = data[data['spatial_cluster'] == cluster]
    
    # brak anomalii
    ax.scatter(cluster_data[cluster_data['anomaly'] == False]['szerokosc'], 
               cluster_data[cluster_data['anomaly'] == False]['dlugosc'], 
               color=cmap(i), label=f'Cluster {cluster}', alpha=0.7)
    
    # anomalie
    ax.scatter(cluster_data[cluster_data['anomaly'] == True]['szerokosc'], 
               cluster_data[cluster_data['anomaly'] == True]['dlugosc'], 
               color=cmap(i), marker='x', edgecolors='k', s=1, 
               label=f'Anomaly in Cluster {cluster}')

ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')

ax.legend()

plt.show()