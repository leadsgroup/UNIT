import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from rtree import index
import time

ti=time.time()

# Read census tracts and noise data
file_name= 'TR_1000ft_LA_60min_All'
census_tracts = gpd.read_file('3combined_data_income.geojson')
noise_data = pd.read_csv('Raw Noise Data/'+file_name+'.csv')

noise_columns = ['L_AeqT', 'L_AeqT_24hr', 'SEL', 'L_dn', 'L_Aeq_jetliner','L_Amax']



threshold_values = {}

# Find minimum value for each noise column
for column in noise_columns:
    threshold_values[column] = noise_data[column].min()

# Create spatial index for noise points
spatial_index = index.Index()
for idx, noise_point in noise_data.iterrows():
    spatial_index.insert(idx, (noise_point['Longitude'] - 360, noise_point['Latitude'], noise_point['Longitude'] - 360, noise_point['Latitude']))

# Create an empty DataFrame to store the maximum noise level for each census tract
max_noise_per_tract = pd.DataFrame(columns=['Latitude', 'Longitude'] + noise_columns)

# Iterate over each noise column
for column in noise_columns:
    max_noise_levels_within_tract = []
    # Iterate through each census tract
    for idx, tract in census_tracts.iterrows():
        tract_polygon = tract['geometry']

        # Get noise points within the current tract using spatial indexing
        possible_matches_idx = list(spatial_index.intersection(tract_polygon.bounds))
        possible_matches = noise_data.iloc[possible_matches_idx]

        # Filter noise points that are within the current tract
        noise_within_tract = possible_matches[possible_matches.apply(lambda row: tract_polygon.contains(Point(row['Longitude'] - 360, row['Latitude'])), axis=1)]

        # Get the maximum noise level within the tract
        if not noise_within_tract.empty:
            max_noise_level = max(noise_within_tract[column], default=threshold_values[column])
            # Append latitude and longitude coordinates of the noise level point
            max_noise_per_tract.loc[idx, column] = max_noise_level
            max_noise_per_tract.loc[idx, 'Latitude'] = noise_within_tract['Latitude'].iloc[0]
            max_noise_per_tract.loc[idx, 'Longitude'] = noise_within_tract['Longitude'].iloc[0] - 360
        else:
            # If no noise points within tract, use the centroid of the tract as the point
            centroid = tract_polygon.centroid
            max_noise_per_tract.loc[idx, column] = threshold_values[column]
            max_noise_per_tract.loc[idx, 'Latitude'] = centroid.y
            max_noise_per_tract.loc[idx, 'Longitude'] = centroid.x

# Save the file
max_noise_per_tract.to_excel(file_name+'max_noise_per_tract.xlsx', index=False)




to = time.time()

print((to-ti)/60)



