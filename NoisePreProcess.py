import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, MultiPoint
import numpy as np
from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon




def process_noise_impact(base_geoJson, noise_filename, output_prefix="Data/", noise_threshold=55):
    census_tracts = gpd.read_file(base_geoJson)
    noise_df = pd.read_csv(noise_filename)

    noise_columns = noise_df.columns[4:]

    noise_df['geometry'] = noise_df.apply(lambda row: Point(row['Longitude'] - 360, row['Latitude']), axis=1)

    noise_gdf = gpd.GeoDataFrame(noise_df, geometry='geometry', crs=census_tracts.crs)

    joined = gpd.sjoin(noise_gdf, census_tracts, how='inner', predicate='within')

    threshold_values = {col: noise_df[col].min() for col in noise_columns}

    mean_noise = joined.groupby('index_right')[noise_columns].mean()
    census_tracts = census_tracts.join(mean_noise)

    for col in noise_columns:
        census_tracts[col] = census_tracts[col].fillna(threshold_values[col])

    # NOISE POINT COUNT (>X dBA)
    joined["L_dn_above_threshold"] = joined["L_dn"] > noise_threshold
    high_noise_count = joined.groupby('index_right')["L_dn_above_threshold"].sum()

    census_tracts["threshold_noise_count"] = (
        census_tracts.index.map(high_noise_count).fillna(0).astype(int))

    # TRACT AREA
    census_tracts["tract_area"] = (census_tracts.geometry.area*(111111**2))


    return census_tracts




def process_DOT_noise(base_geoJson, noise_filename, output_prefix="Data/",noise_threshold=55):


    census_tracts = (base_geoJson)
    noise_df = pd.read_csv(noise_filename)

    # Generate Noise Aggregation and Combine Data

    noise_columns = noise_df.columns[2:]

    noise_df['geometry'] = noise_df.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)

    noise_gdf = gpd.GeoDataFrame(noise_df, geometry='geometry', crs=census_tracts.crs)



    joined = gpd.sjoin(noise_gdf, census_tracts, how='inner', predicate='within')

    threshold_values = {col: noise_df[col].min() for col in noise_columns}

    mean_noise = joined.groupby('index_right')[noise_columns].mean()
    census_tracts = census_tracts.join(mean_noise)

    for col in noise_columns:
        census_tracts[col] = census_tracts[col].fillna(threshold_values[col])

    # NOISE POINT COUNT (>X dBA)
    joined["L_dn_DOT_above_threshold"] = joined["L_dn"] > noise_threshold
    high_noise_count = joined.groupby('index_right')["L_dn_DOT_above_threshold"].sum()
    census_tracts["threshold_noise_count_DOT"] = (
        census_tracts.index.map(high_noise_count).fillna(0).astype(int))

    # SAVE RESULTS
    geojson_out = f"{output_prefix}_Area_Final.geojson"
    csv_out = f"{output_prefix}_Area_Final.csv"

    census_tracts.to_file(geojson_out, driver="GeoJSON")
    results_df = census_tracts.copy()

    drop_cols = ['Latitude', 'Longitude', 'elevation', 'geometry']
    results_df = results_df.drop(columns=[c for c in drop_cols if c in results_df])
    results_df = results_df.loc[:, ~results_df.columns.str.contains('Error', case=False)]


    results_df.to_csv(csv_out, index=False)


    return census_tracts


def sensitive_structs(file_list, census_tracts_file,file_names):
    demo_per_tract = census_tracts_file

    try:
        demo_per_tract = demo_per_tract.drop(['index_right'], axis=1)
    except:
        pass
    i=0
    for file in file_list:
        loc_data = file
        # Convert points to a GeoDataFrame
        loc_data['geometry'] = loc_data.apply(
            lambda row: Point(row['Longitude'], row['Latitude']), axis=1
        )
        loc_gdf = gpd.GeoDataFrame(loc_data, geometry='geometry', crs=demo_per_tract.crs)
        
        # Perform a spatial join to associate points with census tracts
        joined = gpd.sjoin(loc_gdf, demo_per_tract, how='inner', predicate='within')

        # Count points within each census tract
        point_counts = joined.groupby('index_right').size()

        # Add a new column for the point counts to the census tracts GeoDataFrame
        demo_per_tract[file_names[i]] = demo_per_tract.index.map(point_counts).fillna(0).astype(int)
        i+=1

    return demo_per_tract



def process_unique_research_noise(census_tracts_gdf, unique_noise_gdf, output_prefix="Results/"):

    census_tracts_gdf = gpd.read_file(census_tracts_gdf)

    # --- spatial join points within census tracts ---
    joined = gpd.sjoin(unique_noise_gdf, census_tracts_gdf, how="inner", predicate="within")

    # --- count points per tract ---
    noise_count = joined.groupby('index_right').size()
    census_tracts_gdf["noise_count"] = census_tracts_gdf.index.map(noise_count).fillna(0).astype(int)

    census_tracts_gdf["tract_area"] = (census_tracts_gdf.geometry.area*(111111**2))


    # --- save results ---
    geojson_out = f"{output_prefix}_Noise.geojson"
    csv_out = f"{output_prefix}_Noise.csv"

    census_tracts_gdf.to_file(geojson_out, driver="GeoJSON")
    results_df = census_tracts_gdf.copy()

    drop_cols = ['Latitude', 'Longitude', 'elevation', 'geometry']
    results_df = results_df.drop(columns=[c for c in drop_cols if c in results_df])
    results_df = results_df.loc[:, ~results_df.columns.str.contains('Error', case=False)]

    results_df.to_csv(csv_out, index=False)

    return census_tracts_gdf


def difference_noise_pts(dot_noise_file, leads_noise_file, threshold=65, eps=0.01, min_samples=5):
    
    # --- load data ---
    dot_df = pd.read_csv(dot_noise_file)
    research_df = pd.read_csv(leads_noise_file)

    # --- convert to GeoDataFrames ---
    dot_gdf = gpd.GeoDataFrame(
        dot_df,
        geometry=gpd.points_from_xy(dot_df["Longitude"], dot_df["Latitude"]),
        crs="EPSG:4326"
    )
    research_gdf = gpd.GeoDataFrame(
        research_df,
        geometry=gpd.points_from_xy(research_df["Longitude"]-360, research_df["Latitude"]),
        crs="EPSG:4326"
    )

    # --- threshold filter ---
    dot_high = dot_gdf[dot_gdf["value"] > threshold].copy()
    research_high = research_gdf[research_gdf["L_dn"] > threshold].copy()

    # --- ensure CRS match ---
    if dot_high.crs != research_high.crs:
        research_high = research_high.to_crs(dot_high.crs)

    # --- cluster DOT points ---
    coords = np.array(list(dot_high.geometry.apply(lambda p: (p.x, p.y))))
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(coords)
    dot_high['cluster'] = db.labels_  # -1 = noise

    # --- create convex hulls per cluster ---
    hulls = []
    for cluster_id in dot_high['cluster'].unique():
        if cluster_id == -1:
            continue
        cluster_points = dot_high[dot_high['cluster'] == cluster_id]
        hull = MultiPoint(list(cluster_points.geometry)).convex_hull
        hulls.append(hull)

    hulls_gdf = gpd.GeoDataFrame(geometry=hulls, crs=dot_high.crs)

    # --- check which research points are inside any hull ---
    inside_hulls = gpd.sjoin(research_high, hulls_gdf, how='inner', predicate='within')
    unique_pts = research_high[~research_high.index.isin(inside_hulls.index)]
    return unique_pts


def struct_in_contours(geojson,dot_noise_file, leads_noise_file, sens_struct_list,city,p_bounds, threshold=65, eps=0.01, min_samples=5,frequency='NA'):

    dot_df = pd.read_csv(dot_noise_file)
    research_df = pd.read_csv(leads_noise_file)

    # --- convert to GeoDataFrames ---
    dot_gdf = gpd.GeoDataFrame(
        dot_df,
        geometry=gpd.points_from_xy(dot_df["Longitude"], dot_df["Latitude"]),
        crs="EPSG:4326"
    )
    research_gdf = gpd.GeoDataFrame(
        research_df,
        geometry=gpd.points_from_xy(research_df["Longitude"] - 360, research_df["Latitude"]),
        crs="EPSG:4326"
    )

    # --- threshold filter ---
    dot_high = dot_gdf[dot_gdf["value"] > threshold].copy()
    research_high = research_gdf[research_gdf["L_dn"] > threshold].copy()

    # --- cluster  points ---
    coords = np.array(list(dot_high.geometry.apply(lambda p: (p.x, p.y))))
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(coords)
    dot_high['cluster'] = db.labels_

    hulls = []
    for cluster_id in dot_high['cluster'].unique():
        if cluster_id == -1:
            continue
        cluster_points = dot_high[dot_high['cluster'] == cluster_id]
        hull = MultiPoint(list(cluster_points.geometry)).convex_hull
        hulls.append(hull)

    hulls_gdf = gpd.GeoDataFrame(geometry=hulls, crs=dot_high.crs)

    # ---  which points inside any hull ---
    inside_hulls = gpd.sjoin(research_high, hulls_gdf, how='inner', predicate='within')
    unique_pts = research_high[~research_high.index.isin(inside_hulls.index)]


    # cluster unqiue pts
    coords = np.array(list(unique_pts.geometry.apply(lambda p: (p.x, p.y))))
    db = DBSCAN(eps=.0008, min_samples=1).fit(coords)
    unique_pts['cluster'] = db.labels_

    unique_hulls = []
    for cluster_id in unique_pts['cluster'].unique():
        if cluster_id == -1:
            continue
        cluster_points = unique_pts[unique_pts['cluster'] == cluster_id]
        unique_hull = MultiPoint(list(cluster_points.geometry)).convex_hull
        unique_hulls.append(unique_hull)

    unique_hulls_gdf = gpd.GeoDataFrame(geometry=unique_hulls, crs=dot_high.crs)

    # ---  which sensitive structures are inside or near new noise ---
    sens_points_inside = []
    sens_points_new = []

    for i in sens_struct_list:
        i['geometry'] = i.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)
        loc_gdf = gpd.GeoDataFrame(i, geometry='geometry', crs=hulls_gdf.crs)

        inside_hulls = gpd.sjoin(loc_gdf, hulls_gdf, how='inner', predicate='intersects')
        sens_points_inside.append(len(inside_hulls))

        inside_new_noise = gpd.sjoin(loc_gdf, unique_hulls_gdf, how='inner', predicate='intersects')
        sens_points_new.append(len(inside_new_noise))


    # --- make summary dataframe ---
    summary_data = pd.DataFrame({
        'City': city,
        'Frequency': frequency,
        'Threshold': threshold,
        'Category': ['Schools', 'Places of Worship', 'Hospitals'],
        'Existing_Affected': sens_points_inside,
        'Newly_Affected': sens_points_new
    })



    # --- PLOTTING ---
    fig, ax = plt.subplots(figsize=(10, 10))
    hulls_gdf.plot(
        ax=ax,
        edgecolor='red',
        facecolor='none',
        linewidth=2,
        label=f'Noise Countour Hull> {threshold} dBA'
    )
    unique_pts.plot(ax=ax,
        color='purple',
        alpha=.5,
        label='new noise'
        )
    
    unique_hulls_gdf.plot(
        ax=ax,
        edgecolor='blue',
        facecolor='none',
        linewidth=2,
        label=f'Noise Countour Hull> {threshold} dBA'
    )
    
    
    # Plot sensitive structures
    names = ['school','churches','hospitals']
    for idx, i in enumerate(sens_struct_list):
        loc_gdf = gpd.GeoDataFrame(i, geometry='geometry', crs=hulls_gdf.crs)
        loc_gdf.plot(ax=ax, marker='*', markersize=50, alpha=.5,label=f'{names[idx]}')
    geojson = gpd.read_file(geojson)
    geojson.plot( ax=ax,
                    edgecolor='black', 
                    facecolor = 'none',
                    alpha=.5,
                    linewidth=0.15)

    min_x, min_y, max_x, max_y = p_bounds.bounds


    ax.legend()
    ax.set_xlim(min_x,max_x)
    ax.set_ylim(min_y,max_y)
    ax.set_title(f"{threshold} dBA")
    plt.savefig(f'JournalPlots/{city}_Struct_{threshold}.png',dpi=600)

    return summary_data
