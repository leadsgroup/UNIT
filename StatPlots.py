import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import pandas as pd
import os
import numpy as np

# Read the noise data and census data
gdf_census = gpd.read_file('3combined_data_race.geojson')
types = ['HC','SR','TR']
# timesteps = ['10','30','60']
# noise_columns = ['L_AeqT', 'L_AeqT_24hr', 'SEL', 'L_dn', 'L_Aeq_jetliner','L_Amax']

noise_columns = ['L_AeqT']
timesteps = ['10']

threshold_vals = [85]


# threshold_vals = [85, 85, 85, 85, 85, 85]

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

        
        for noise_type, threshold_val in zip(noise_columns, threshold_vals):
            upper_quartile = np.nanpercentile(merged_gdf[noise_type],75)
            upper_quartile_rnd = round(upper_quartile,2)
            threshold_val = upper_quartile_rnd
            # Filter tracts with noise levels over the threshold value
            high_noise_tracts = merged_gdf[merged_gdf[noise_type] > threshold_val]

            # Calculate the percentage of Hispanic and Black population in high noise tracts
            high_noise_tracts_total_pop = high_noise_tracts['B03002001'].sum()
            percentage_hispanic_population = high_noise_tracts['B03002012'].sum()# / high_noise_tracts_total_pop * 100
            percentage_black_population = high_noise_tracts['B03002004'].sum() #/ high_noise_tracts_total_pop * 100
            percentage_asian_population = high_noise_tracts['B03002006'].sum() #/ high_noise_tracts_total_pop * 100
            percentage_white_population = high_noise_tracts['B03002003'].sum() #/ high_noise_tracts_total_pop * 100



            #B03002003 white alone
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

            # Calculate the total percentage of Hispanics and Black in the census data
            # total_hispanic_percentage = (total_hispanic_population / total_population) * 100
            # total_black_percentage = (total_black_population / total_population) * 100
            # total_asian_percentage =(total_asian_population/total_population)*100
            # total_white_percentage =(total_white_population/total_population)*100
            

            
            folder_path2 = 'BarImages_75thpercentile_Report/'

            # Check if the folder exists, and if not, create it
            if not os.path.isdir(folder_path2):
                os.mkdir(folder_path2)
            hispanic_pop_total = (high_noise_tracts['B03002012'].sum()/total_hispanic_population)*100

            black_pop_total = (high_noise_tracts['B03002004'].sum() /total_black_population)*100

            asian_pop_total = (high_noise_tracts['B03002006'].sum() /total_asian_population)*100

            white_pop_total =  (high_noise_tracts['B03002003'].sum() /total_white_population)*100

            import matplotlib.pyplot as plt

            plt.figure(figsize=(10, 8))

            data_groups = ['$\mathrm{Hispanic_{LA\,Area}}$', '$\mathrm{Hispanic_{Noise\,Path}}$',
                        '$\mathrm{Black_{LA\,Area}}$', '$\mathrm{Black_{Noise\,Path}}$', 
                        '$\mathrm{Asian_{LA\,Area}}$', '$\mathrm{Asian_{Noise\,Path}}$', 
                        '$\mathrm{White_{LA\,Area}}$', '$\mathrm{White_{Noise\,Path}}$']

            grp_precentages = [total_hispanic_population, percentage_hispanic_population,
                            total_black_population, percentage_black_population,
                            total_asian_population, percentage_asian_population,
                            total_white_population, percentage_white_population]

            colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#9467bd', '#c5b0d5']

            # Plotting
            plt.bar(data_groups, grp_precentages, color=colors, label =data_groups)

            plt.title("Total Percentage of Demographic Impacted by " + actype + ' ' + noise_type + ' > ' + str(threshold_val) + 'dB for ' + timeval + ' min')
            plt.xlabel("Demographic")
            plt.ylabel("Total of Demographic")
            plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
            plt.tight_layout()
            plt.legend()

            # Save the combined plot
            plt.savefig(os.path.join(folder_path2, actype+'_1000ft_LA_'+timeval+'min'+'_'+noise_type + 'barplot.png'))



            # folder_path = 'BarImages/'

            # # Check if the folder exists, and if not, create it
            # if not os.path.isdir(folder_path):
            #     os.mkdir(folder_path)

            # plt.figure(figsize=(10, 8))
            
            # # Define data for plotting
            # population_groups = ['Total Hispanic Population Percentage', 'Hispanic Population Percentage\n in High Noise Tracts',
            #                     'Total Black Population Percentage', 'Black Population Percentage\n in High Noise Tracts',
            #                     'Total Asian Population Percentage', 'Asian Population Percentage\n in High Noise Tracts']
            # percentages = [total_hispanic_percentage, percentage_hispanic_population,
            #                total_black_percentage, percentage_black_population,
            #                total_asian_percentage, percentage_asian_population]

            # # Generate random colors
            # np.random.seed(0)
            # colors = np.random.rand(len(population_groups), 3)

            # # Plot horizontal bar plot with random colors
            # bars = plt.bar(population_groups, percentages, color=colors)

            # plt.title("Evaluation of Noise Affected Populations for " + noise_type + '>' + str(threshold_val) + 'dB')
            # plt.xlabel("Percentage")
            # plt.ylabel("Population")
            # plt.tight_layout()

            # # Add legend
            # plt.legend(bars, population_groups)

            # # Save the combined plot
            # plt.savefig(os.path.join(folder_path, actype+'_1000ft_LA_'+timeval+'min'+'_'+noise_type + 'barplot.png'))
