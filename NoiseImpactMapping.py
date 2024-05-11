import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import pandas as pd
import plotly.graph_objects as go
import os

# Read the noise data and census data
gdf_census = gpd.read_file('3combined_data_race.geojson')

# Define the bounding box coordinates
min_lon, max_lon = -119, -117
min_lat, max_lat = 33, 34.5

# Filter the census data based on bounding box
bbox_polygon = Polygon([(min_lon, min_lat), (max_lon, min_lat), (max_lon, max_lat), (min_lon, max_lat)])
gdf_census_inside_bbox = gdf_census[gdf_census['geometry'].intersects(bbox_polygon)]

types = ['HC','SR','TR']
timesteps = ['10','30','60']
noise_columns = ['SEL']

for actype in types:
    for timeval in timesteps:
        file_name = actype + '_1000ft_LA_' + timeval + 'min_Allmax_noise_per_tract.xlsx'
        noise_data = pd.read_excel('Filtered noise data/' + file_name)
        
        # Create a GeoDataFrame from the filtered noise data
        geometry = [Point(xy) for xy in zip(noise_data['Longitude'], noise_data['Latitude'])]
        noise_gdf = gpd.GeoDataFrame({'Latitude': noise_data['Latitude'],
                                       'Longitude': noise_data['Longitude'],
                                       'L_Amax': noise_data['L_Amax'],
                                       'L_AeqT': noise_data['L_AeqT'],
                                       'L_AeqT_24hr': noise_data['L_AeqT_24hr'],
                                       'SEL': noise_data['SEL'],
                                       'L_dn': noise_data['L_dn'],
                                       'L_Aeq_jetliner': noise_data['L_Aeq_jetliner']},
                                      geometry=geometry, crs='EPSG:4326')

        # Perform a spatial join to combine the filtered census geometries with the filtered noise data
        merged_gdf_inside_bbox = gpd.sjoin(gdf_census_inside_bbox, noise_gdf.set_geometry('geometry'), how='left', op='contains')

        folder_path = 'PlotImages' + actype + '/'

        # Check if the folder exists, and if not, create it
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)

        # Define the data types to plot
        data_types = ['L_Amax', 'L_AeqT', 'L_AeqT_24hr', 'SEL', 'L_dn', 'L_Aeq_jetliner']

        # Plot chloropleth maps for each data type
        for data_columns in data_types:
            plt.figure(figsize=(20, 15))
            merged_gdf_inside_bbox.plot(column=data_columns,  # Use the data column
                                         cmap='RdYlGn_r',
                                         edgecolor='white',
                                         linewidth=0.15,
                                         alpha=0.75,
                                         legend=True,
                                         legend_kwds={"label": "Noise Level (dB)", "orientation": "vertical"},
                                         )

            plt.title(data_columns)
            plt.savefig(os.path.join(folder_path, data_columns + actype+timeval+'.png'))

# race_data = ['Percent Non Hispanic White alone',
#        'Percent Non Hispanic Black or African American alone',
#        'Percent Non Hispanic American Indian and Alaska Native alone',
#        'Percent Non Hispanic Asian alone',
#        'Percent Non Hispanic Native Hawaiian and Other Pacific Islander alone',
#        'Percent Non Hispanic Some Other Race alone',
#        'Percent Non Hispanic Two or More Races', 'Percent Hispanic or Latino']
# income_data = ['Less than $10,000', '$10,000 to $14,999',
#        '$15,000 to $19,999', '$20,000 to $24,999', '$25,000 to $29,999',
#        '$30,000 to $34,999', '$35,000 to $39,999', '$40,000 to $44,999',
#        '$45,000 to $49,999', '$50,000 to $59,999', '$60,000 to $74,999',
#        '$75,000 to $99,999', '$100,000 to $124,999', '$125,000 to $149,999',
#        '$150,000 to $199,999', '$200,000 or more']
