import geopandas as gpd
from shapely.geometry import Point
import plotly.express as px

def generate_noise_map(noise_df, selected_noise_level, noise_type):
    # Load the custom census tract data (GeoJSON format)
    gdf_custom_tracts = gpd.read_file(r'C:\Users\Yair\OneDrive\Documents\Yair\Research\UNIT\Raw_Data\filtered_race_data_lacounty.geojson')

    # Create a GeoDataFrame from noise_df using latitude and longitude for geometry
    noise_df['geometry'] = gpd.points_from_xy(noise_df['Longitude'], noise_df['Latitude'])
    noise_gdf = gpd.GeoDataFrame(noise_df, geometry='geometry', crs='EPSG:4326')

    # Filter the noise data based on selected noise level and noise type
    filtered_noise_gdf = noise_gdf[noise_gdf[noise_type] >= selected_noise_level]
    # filtered_noise_gdf = noise_gdf

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
        labels={noise_type: 'Noise Level (dB)'},
        title=f'{noise_type} above {selected_noise_level} dB'
    )

    return fig
