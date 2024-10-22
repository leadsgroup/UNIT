# load the shape file for LA County boundary
file_path = '/Users/avacipriani/Desktop/LEADS/UNIT/Processed_Data/data race la county/Edited_CensusData_LACounty_filtered.geojson'

# function to generate a simple LA County boundary plot
def generate_la_county_plot():
    
    # load the GeoJSON file
    boundary_gdf = gpd.read_file(file_path)
    
    # create a plot of LA County boundaries
    fig, ax = plt.subplots(figsize=(12, 12))
    boundary_gdf.plot(ax=ax, color='lightgrey', edgecolor='black')
    
    ax.set_title('LA County Boundary')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_aspect('equal')
    
    # save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    
    # encode the image as Base64 to display in Dash
    encoded_img = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{encoded_img}"

# DONT RUN THIS ITS NOT FINISHED