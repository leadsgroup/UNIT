import geopandas as gpd
from shapely.geometry import Point
import plotly.express as px
import os 

separator = os.path.sep 
# Update the filenames for geojson data 
gdf_custom_tracts = '..' + separator + 'Raw_Data' + separator + 'filtered_race_data_lacounty.geojson' 
# Load the custom census tract data (GeoJSON format) 
gdf_custom_tracts = gpd.read_file(gdf_custom_tracts)

def generate_noise_map(noise_df, selected_noise_level, noise_type):

    # Create a GeoDataFrame from noise_df using latitude and longitude for geometry
    noise_df['geometry'] = gpd.points_from_xy(noise_df['Longitude'], noise_df['Latitude'])
    noise_gdf = gpd.GeoDataFrame(noise_df, geometry='geometry', crs='EPSG:4326')

    # Filter the noise data based on selected noise level and noise type
    filtered_noise_gdf = noise_gdf[noise_gdf[noise_type] >= selected_noise_level]

    # Perform spatial join with census tracts
    merged_gdf = gpd.sjoin(gdf_custom_tracts, filtered_noise_gdf).to_crs(4326)

    # Create the choropleth map
    fig = px.choropleth_mapbox(
        merged_gdf,
        geojson=gdf_custom_tracts,  # Use the GeoJSON format
        locations='name',  # Use the unique identifier for locations
        featureidkey='properties.name',
        color=noise_type,
        color_continuous_scale='plasma',
        center={"lat": 34, "lon": -118},  # Center over Los Angeles
        mapbox_style="carto-positron",
        labels={noise_type: 'Noise Level (dB)'}
    )
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    
    return fig
