import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import pandas as pd
#this code reads the noise data csv to organize it in order to combine with the census data
noise_data = pd.read_csv('path_to_your_csv_file.csv')

# Create a GeoDataFrame from the CSV noise data
#add more  columns based on csv data for more noise data to plot and compare
geometry = [Point(xy) for xy in zip(noise_data['longitudes'], noise_data['latitudes'])]
noise_gdf = gpd.GeoDataFrame({'Latitude': noise_data['latitudes'],
                              'Longitude': noise_data['longitudes'],
                              'Intensity': noise_data['Intensity']},
                              #add any additional columns of data here
                             geometry=geometry, crs='EPSG:4326')


#existing code to read GeoJSON file and create GeoDataFrames
gdf_census = gpd.read_file('CensusDataPath')

# Perform a spatial join to combine the census geometries with the highest noise data
merged_gdf = gpd.sjoin(gdf_census, noise_gdf.set_geometry('geometry'), how='left', op='contains')

# Create 1 x 1 subplot
#This code allows you to add  subplots to compare noise data impact by adding another ax like ax2
#then using the same method as showed for noise intensity to get a chloropleth map of the data
fig, ax1 = plt.subplots(1, 1, figsize=(15, 12))

# Plot with the highest intensity per GeoID polygon
merged_gdf.plot(column='Intensity',  # Use the aggregated intensity column
                cmap='RdYlGn_r',
                k=1,#K=1 means one bin only for each tract and will therfore showcase the largest data point regardless of the other points
                edgecolor='white',
                linewidth=0.0,
                alpha=0.75,
                ax=ax1,
                legend=True)
ax1.axis("off")
ax1.set_title("Highest Intensity per GeoID Polygon")

plt.show()
