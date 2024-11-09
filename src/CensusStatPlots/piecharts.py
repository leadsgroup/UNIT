import pandas as pd
import plotly.express as px
import geopandas as gpd
from shapely.geometry import Point
import plotly.express as px

def generate_pie_chart(noise_df, noise_level_pc, noise_type_dropdown_pc, Census_Data):
    income_data_sheet,race_data_sheet=Census_Data
    # Convert noise_df to GeoDataFrame with Point geometry from Latitude and Longitude
    noise_df['geometry'] = gpd.points_from_xy(noise_df['Longitude'], noise_df['Latitude'])
    noise_gdf = gpd.GeoDataFrame(noise_df, geometry='geometry')

    # Filter noise data based on noise level and type
    filtered_noise_data = noise_gdf[noise_gdf[noise_type_dropdown_pc] >= noise_level_pc]

    # Ensure both census GeoDataFrames and noise GeoDataFrame have the same CRS (coordinate reference system)
    income_data_sheet = income_data_sheet.set_crs(filtered_noise_data.crs, allow_override=True)
    race_data_sheet = race_data_sheet.set_crs(filtered_noise_data.crs, allow_override=True)

    # Spatial join to find areas in race and income data within or near the filtered noise locations
    filtered_race_data = gpd.sjoin(race_data_sheet, filtered_noise_data, how="inner", predicate="intersects")
    filtered_income_data = gpd.sjoin(income_data_sheet, filtered_noise_data, how="inner", predicate="intersects")

     # Calculate total population in filtered race data for percentage calculation
    total_population = filtered_race_data['Total Population'].sum()

    # Calculate race percentages based on filtered data
    race_percentages = {
        'Race': ['Hispanic/Latino', 'Black/African American', 'White'],
        'Percentage': [
            filtered_race_data['Hispanic or Latino'].sum() / total_population * 100,
            filtered_race_data['Black or African American'].sum() / total_population * 100,
            filtered_race_data['White'].sum() / total_population * 100
        ]
    }
    race_data = pd.DataFrame(race_percentages)

    # Calculate total households in filtered income data for percentage calculation
    total_households = filtered_income_data['Total Households'].sum()

    # Calculate income percentages based on filtered data
    income_percentages = {
        'Income Range': [
            '0-30,000', '30,000-60,000', '60,000-90,000', '90,000-100,000'
        ],
        'Percentage': [
            filtered_income_data['0-30,000'].sum() / total_households * 100,
            filtered_income_data['30,000-60,000'].sum() / total_households * 100,
            filtered_income_data['60,000-90,000'].sum() / total_households * 100,
            filtered_income_data['90,000-100,000'].sum() / total_households * 100
        ]
    }
    income_data = pd.DataFrame(income_percentages)

    # Plot race distribution pie chart
    race_pie = px.pie(race_data, names='Race', values='Percentage', 
                      title='Race Distribution',
                      color_discrete_sequence=['#636EFA', '#EF553B', '#00CC96'])
    race_pie.update_traces(textinfo='percent+label', hoverinfo='label+percent', hole=.4)
    race_pie.update_layout(title_font_size=11, font_size=9)

    # Plot income distribution pie chart
    income_pie = px.pie(income_data, names='Income Range', values='Percentage', 
                        title='Income Distribution',
                        color_discrete_sequence=['#636EFA', '#EF553B', '#00CC96'])
    income_pie.update_traces(textinfo='percent+label', hoverinfo='label+percent', hole=.4)
    income_pie.update_layout(title_font_size=11, font_size=9)

    return race_pie, income_pie