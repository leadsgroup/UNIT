import pandas as pd
import plotly.express as px
import os
import geopandas as gpd

separator = os.path.sep 

# Update the filenames for geojson data 
income_tracts = '..' + separator + 'Processed_Data' + separator + 'income.geojson' 
race_tracts = '..' + separator + 'Processed_Data' + separator + 'race.geojson' 

# Load the custom census tract data (GeoJSON format) 
income_tracts = gpd.read_file(income_tracts)
race_tracts = gpd.read_file(race_tracts)

def generate_pie_chart(noise_df, noise_level_pc, noise_type_dropdown_pc):

    # Create a GeoDataFrame from noise_df using latitude and longitude for geometry
    noise_df['geometry'] = gpd.points_from_xy(noise_df['Longitude'], noise_df['Latitude'])
    noise_gdf = gpd.GeoDataFrame(noise_df, geometry='geometry', crs='EPSG:4326')


    # Filter the noise data based on selected noise level and noise type
    filtered_noise_gdf = noise_gdf[noise_gdf[noise_type_dropdown_pc] >= noise_level_pc]

    # Perform spatial join with census tracts
    merged_income_gdf = gpd.sjoin(income_tracts, filtered_noise_gdf, how='inner').to_crs(4326)
    merged_race_gdf = gpd.sjoin(race_tracts, filtered_noise_gdf, how='left').to_crs(4326)


    total_population = merged_race_gdf['B03002001'].sum()  # Total population column

    race_percentages = {
        'Race': ['Hispanic/Latino', 'Black/African American', 'White', 'Asian'],
        'Percentage': [
            merged_race_gdf[['B03002012']].sum(axis=1).sum() / total_population * 100,  # Hispanic/Latino
            merged_race_gdf[['B03002004']].sum(axis=1).sum() / total_population * 100,  # Black or African American 
            merged_race_gdf[['B03002003']].sum(axis=1).sum() / total_population * 100,  # White
            merged_race_gdf[['B03002006']].sum(axis=1).sum() / total_population * 100   # Asian
        ]
    }
    
    race_data = pd.DataFrame(race_percentages)

    # Calculate income percentages based on B19001 codes (income categories)
    total_households = merged_income_gdf['B19001001'].sum()  # Total households column

    income_percentages = {
        'Income Range': ['0-30k;', '30k-60k', '60k-75k', '75k-100k', '100k-125k','125k-150k','150k-200k','200k+'],
        'Percentage': [
            merged_income_gdf[['B19001002','B19001003','B19001004','B19001005','B19001006']].sum(axis=1).sum() / total_households * 100,  # 0-30k 
            merged_income_gdf[['B19001007','B19001008','B19001009','B19001010','B19001011',]].sum(axis=1).sum() / total_households * 100,  # 30k-60k 
            merged_income_gdf[['B19001012']].sum(axis=1).sum() / total_households * 100,  # 60k-75k 
            merged_income_gdf[['B19001013']].sum(axis=1).sum() / total_households * 100,  # 75k-100k 
            merged_income_gdf[['B19001014']].sum(axis=1).sum() / total_households * 100,  # 100k-125k
            merged_income_gdf[['B19001015']].sum(axis=1).sum() / total_households * 100,  # 125k-150k
            merged_income_gdf[['B19001016']].sum(axis=1).sum() / total_households * 100,  # 150k-200k
            merged_income_gdf[['B19001017']].sum(axis=1).sum() / total_households * 100   # 200k+ 
        ]
    }

    income_data = pd.DataFrame(income_percentages)

    # Plot race distribution pie chart
    race_pie = px.pie(race_data, names='Race', values='Percentage', 
                      title='Race Distribution')

    # Plot income distribution pie chart
    income_pie = px.pie(income_data, names='Income Range', values='Percentage', 
                        title='Income Distribution')
    

    return race_pie, income_pie
