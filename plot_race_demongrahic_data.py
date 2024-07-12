 import geopandas as gpd 
import contextily as ctx 
import matplotlib.pyplot as plt 
import json 
import geopandas as gpd


def main():
    
    gdf = gpd.read_file('PrePercentage_CombinedRaceData.geojson')
    gdf.plot(figsize = (12, 10),
             column = 'Percent Non Hispanic Black or African American alone',
             legend = True)
    
    
    # load a data file
    # note the relative filepath. edit to fit where the file is located on your computer
    
    la_gdf = gpd.read_file('data la county edited/Edited_CensusData_LACounty_filtered.geojson')
    sanbernardino_gdf = gpd.read_file('data san bernardino county edited/Edited_CensusData_SanBernardino.geojson')
    orange_gdf = gpd.read_file('data orange county edited/Edited_CensusData_OrangeCounty.geojson')
    riverside_gdf = gpd.read_file('data riverside county edited/Edited_CensusData_RiversideCounty.geojson')
    
    
    # Plot for Los Angeles County
    plt.figure(figsize=(12, 10))
    la_gdf.plot(column='Percent Non Hispanic Black or African American alone', legend=True)
    plt.title("Los Angeles County: Percent Non Hispanic\nBlack or African American alone")
    plt.show()
    
    # Plot for San Bernardino County
    plt.figure(figsize=(12, 10))
    sanbernardino_gdf.plot(column='Percent Non Hispanic Black or African American alone', legend=True)
    plt.title("San Bernardino County: Percent Non Hispanic\nBlack or African American alone")
    plt.show()
    
    # Plot for Orange County
    plt.figure(figsize=(12, 10))
    orange_gdf.plot(column='Percent Non Hispanic Black or African American alone', legend=True)
    plt.title("Orange County: Percent Non Hispanic\nBlack or African American alone")
    plt.show()
    
    # Plot for Riverside County
    plt.figure(figsize=(12, 10))
    riverside_gdf.plot(column='Percent Non Hispanic Black or African American alone', legend=True)
    plt.title("Riverside County: Percent Non Hispanic\nBlack or African American alone")
    plt.show()
    
    # Combine all three GeoDataFrames into one
    combined_gdf = pd.concat([la_gdf, sanbernardino_gdf, orange_gdf, riverside_gdf], ignore_index=True)
    
    # Plot the combined GeoDataFrame
    combined_gdf.plot(figsize=(12, 10),
                      column='Percent Non Hispanic Black or African American alone',
                      legend=True)
    plt.title("Percent Non Hispanic Black or African American alone")
    plt.show()
    
    combined_gdf.to_file('3combined_data_race.geojson', driver='GeoJSON')
    
    
    # create 1 x 3 subplots
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    
    # name each subplot
    ax1, ax2, ax3 = axs
    
    # Define the color scale range
    vmin = 0
    vmax = 100
    
    # Plotting on the first subplot
    combined_gdf.plot(column='Percent Hispanic or Latino',
                      cmap='RdYlGn_r',
                      k=5,
                      edgecolor='white',
                      linewidth=0.0,
                      alpha=0.75,
                      ax=ax1,
                      legend=True,
                      vmin=vmin,
                      vmax=vmax)
    ax1.axis("off")
    ax1.set_title("Percent Hispanic or Latino")
    
    # Plotting on the second subplot
    combined_gdf.plot(column="Percent Non Hispanic Black or African American alone",
                      cmap='RdYlGn_r',
                      k=5,
                      edgecolor='white',
                      linewidth=0.0,
                      alpha=0.75,
                      ax=ax2,
                      legend=True,
                      vmin=vmin,
                      vmax=vmax)
    ax2.axis("off")
    ax2.set_title("Percent Non Hispanic Black")
    
    # Plotting on the third subplot
    combined_gdf.plot(column="Percent Non Hispanic White alone",
                      cmap='RdYlGn_r',
                      k=5,
                      edgecolor='white',
                      linewidth=0.0,
                      alpha=0.75,
                      ax=ax3,
                      legend=True,
                      vmin=vmin,
                      vmax=vmax)
    ax3.axis("off")
    ax3.set_title("Percent Non Hispanic White") 
    
    return 


if __name__ == '__main__':
    main() 
    plt.show()
