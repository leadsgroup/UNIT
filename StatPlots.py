import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import pandas as pd
import os
import numpy as np

# Read the noise data and census data
gdf_census = gpd.read_file('3combined_data_race.geojson')
types = ['HC','SR','TR']

noise_columns = ['L_AeqT']
timesteps = ['10']


# Define the bounding box coordinates
min_lon, max_lon = -119, -117
min_lat, max_lat = 33, 34.5

# Filter the census data based on the bounding box
bbox_polygon = Polygon([(min_lon, min_lat), (max_lon, min_lat), (max_lon, max_lat), (min_lon, max_lat)])
gdf_census_inside_bbox = gdf_census[gdf_census['geometry'].intersects(bbox_polygon)]

for actype in types:
    for timeval in timesteps:
        file_name= actype+'_1000ft_LA_'+timeval+'min_Allmax_noise_per_tract.xlsx'
        noise_data = pd.read_excel('Filtered noise data/'+file_name)
        
        # Create GeoDataFrames for noise data
        geometry = [Point(xy) for xy in zip(noise_data['Longitude'], noise_data['Latitude'])]
        noise_gdf = gpd.GeoDataFrame(noise_data, geometry=geometry, crs='EPSG:4326')

        # Perform a spatial join to combine the census geometries with the noise data
        merged_gdf = gpd.sjoin(gdf_census_inside_bbox, noise_gdf, how='left', op='contains')

        
        for noise_type in noise_columns:
            upper_quartile = np.nanpercentile(merged_gdf[noise_type],75)
            upper_quartile_rnd = round(upper_quartile,2)
            threshold_val = upper_quartile_rnd

            # Filter tracts with noise levels over the threshold value
            high_noise_tracts = merged_gdf[merged_gdf[noise_type] > threshold_val]

            # Calculate the percentage of Hispanic and Black population in high noise tracts
            high_noise_tracts_total_pop = high_noise_tracts['B03002001'].sum()
            high_noise_tracts_hispanic_population = high_noise_tracts['B03002012'].sum()
            high_noise_tracts_black_population = high_noise_tracts['B03002004'].sum() 
            high_noise_tracts_asian_population = high_noise_tracts['B03002006'].sum() 
            high_noise_tracts_white_population = high_noise_tracts['B03002003'].sum() 


            #Census codes
            # B03002003 white alone
            # B03002004 black or african american
            # B03002005 American Indian and Alaska Native
            # B03002006 asian
            # B03002007 Native Hawaian and Other Pacific Islander alone

            # Calculate the total Hispanic and Black population for the entire area
            total_population = gdf_census_inside_bbox['B03002001'].sum()
            total_hispanic_population = gdf_census_inside_bbox['B03002012'].sum()
            total_black_population = gdf_census_inside_bbox['B03002004'].sum()
            total_asian_population = gdf_census_inside_bbox['B03002006'].sum()
            total_white_population = gdf_census_inside_bbox['B03002003'].sum()
            
            folder_path2 = 'BarImages_75thpercentile_Report/'

            # Check if the folder exists, and if not, create it
            if not os.path.isdir(folder_path2):
                os.mkdir(folder_path2)

            # Data
            data_groups = ['$\mathrm{Hispanic_{LA\,Area}}$', '$\mathrm{Hispanic_{Noise\,Path}}$',
                        '$\mathrm{Black_{LA\,Area}}$', '$\mathrm{Black_{Noise\,Path}}$', 
                        '$\mathrm{Asian_{LA\,Area}}$', '$\mathrm{Asian_{Noise\,Path}}$', 
                        '$\mathrm{White_{LA\,Area}}$', '$\mathrm{White_{Noise\,Path}}$']


            # Colors for plot
            colors = ['#1f77b4', '#aec7e8']

            # Starting Plot
            plt.figure(figsize=(12, 10))

            # Grouping data 
            labels = ['Hispanic', 'Black', 'Asian', 'White']
            la_area_values = [total_hispanic_population, total_black_population, total_asian_population, total_white_population]
            noise_path_values = [high_noise_tracts_hispanic_population, 
                                 high_noise_tracts_black_population,
                                 high_noise_tracts_asian_population,
                                 high_noise_tracts_white_population]

            #Total amount of columns to create evenly spaced plots
            x = range(len(labels))

            plt.bar([i - 0.2 for i in x], la_area_values, width=0.4, color=colors[0], align='center', label='LA Area')
            plt.bar([i + 0.2 for i in x], noise_path_values, width=0.4, color=colors[1], align='center', label='Noise Path')

            # Adding titles and labels
            plt.title("Total Percentage of Demographic Impacted by " + actype + ' ' + noise_type + ' > ' + str(threshold_val) + 'dB for ' + timeval + ' min',fontsize=15)
            plt.xlabel("Demographic",fontsize=20)
            plt.ylabel("Total of Demographic",fontsize=20)
            plt.xticks(x, labels, ha='right',fontsize=15)  
            plt.tight_layout()
            plt.legend(fontsize=15)

            # Save the combined plot
            plt.savefig(os.path.join(folder_path2, actype+'_1000ft_LA_'+timeval+'min'+'_'+noise_type + 'barplot.png'))
