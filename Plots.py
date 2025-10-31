import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from shapely.geometry import MultiPoint
from sklearn.cluster import DBSCAN
import matplotlib as mpl
from matplotlib.lines import Line2D
import seaborn as sns
from shapely.geometry import Point, Polygon
import matplotlib.cm as cm
import matplotlib.colors as mcolors

def compute_single_households(file):
    file['Total Households'] = file['B25136003'] + file['B25136004']
    return file

def compute_impacted(df, density):
    microphones = round(df['tract_area'] * density)
    impacted = df['noise_count'] / microphones * df['Total Households']
    return round(impacted.sum())

def compute_impacted_areas(df, density):
    microphones = round(df['tract_area'] * density)
    impacted = df['noise_count'] / microphones * df['Total Households']
    return (impacted)


def plot_line_costs(thresholds, med_costs, high_costs, med_err, high_err, save_path):
    plt.figure(figsize=(8, 8))
    plt.errorbar(thresholds, med_costs, yerr=med_err, fmt='-o', capsize=5, linewidth=1, label='Medium Frequency')
    plt.errorbar(thresholds, high_costs, yerr=high_err, fmt='-s', capsize=5, linewidth=1, label='High Frequency')
    plt.xlabel('Noise Threshold (dBA)')
    plt.ylabel('Estimated Cost (Millions $)')
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=900)
    plt.close()

def plot_homes_impacted(thresholds, city_costs, frequency, save_path):
    viridis = cm.get_cmap('Paired')
    colors = [viridis(i / len(frequency)) for i in range(len(frequency))]
    
    viridis = cm.get_cmap('Paired')
    color_med = viridis(0.1) 
    color_high = viridis(0.3)

    colors=[color_med,color_high]
    
    markers = ['o', 's', 'D', '^', 'v', 'P', '*']

    plt.figure(figsize=(8, 8))
    plt.rcParams['axes.linewidth'] = 2.0
    plt.rcParams["font.family"] = "Times New Roman"
    parameters = {
        'axes.labelsize': 16,
        'xtick.labelsize': 14,
        'ytick.labelsize': 14,
        'axes.titlesize': 0,
        'xtick.major.pad': 1,
        'ytick.major.pad': 0}
    plt.rcParams.update(parameters)

    for idx, operation in enumerate(city_costs):
        plt.plot(
            thresholds,
            operation,
            f'-{markers[idx % len(markers)]}',  
            color=colors[idx],
            label=f'{frequency[idx]} Frequency',
            linewidth=2,
            markersize=6,)

    plt.xlabel('Noise Threshold (dBA)')
    plt.ylabel('Estimated Single-Unit Homes Impacted')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=900)
    plt.close()


def hull_plots(DOT_Noise,geojson,bounds,threshold,city):
    dot_noise_file = pd.read_csv(DOT_Noise)
    base_geojson = gpd.read_file(geojson)

    dot_gdf = gpd.GeoDataFrame(
        dot_noise_file,
        geometry=gpd.points_from_xy(dot_noise_file["Longitude"], dot_noise_file["Latitude"]),
        crs="EPSG:4326")
    dot_high = dot_gdf[dot_gdf["value"] > threshold].copy()

    coords = np.array(list(dot_high.geometry.apply(lambda p: (p.x, p.y))))

    db = DBSCAN(eps=0.01, min_samples=5).fit(coords)
    dot_high['cluster'] = db.labels_  # -1 = noise

    hulls = []
    for cluster_id in dot_high['cluster'].unique():
        if cluster_id == -1:
            continue  # skip noise points
        cluster_points = dot_high[dot_high['cluster'] == cluster_id]
        hull = MultiPoint(list(cluster_points.geometry)).convex_hull
        hulls.append(hull)

    hulls_gdf = gpd.GeoDataFrame(geometry=hulls, crs=dot_high.crs)

    fig, ax = plt.subplots(figsize=(12, 12))

    base_geojson.plot( ax=ax,
                    edgecolor='black', 
                    facecolor='none',
                    alpha=.5,
                    linewidth=0.25)

    sc=dot_gdf.plot(ax=ax, column='value',cmap='viridis', markersize=5, label='L_dn', legend=True,vmin=45,vmax=90)

    cbar = sc.get_figure().get_axes()[-1]
    cbar.set_ylabel("Noise Level (dBA)", fontsize=10)

    hulls_gdf.plot(ax=ax,edgecolor='red',facecolor='none',linewidth=2,label=f'Noise Countour Hull> {threshold} dBA')

    # Plot settings
    ax.set_xlabel("Longitude", fontsize=12)
    ax.set_ylabel("Latitude", fontsize=12)
    ax.set_xlim(bounds[0],bounds[2])
    ax.set_ylim(bounds[1],bounds[3])
    #custom legend to showcase hulls
    custom_legend = [
    Line2D([0], [0], color='red', lw=2, label=f'Noise Contour Hull > {threshold} dBA')]
    ax.legend(handles=custom_legend, loc='upper right')

    plt.savefig(f'JournalPlots/{city}_{threshold}_hulls.png',dpi=600)
    plt.close()

    return

def struct_stats_barplot(stat_file, city):

    df = pd.read_csv(stat_file)

    for category in df['Category'].unique():
        cat_df = df[df['Category'] == category]

        pivot_df = cat_df.pivot_table(
            index='Threshold',
            columns='Frequency',
            values=['Existing_Affected', 'Newly_Affected'],
            aggfunc='first')

        pivot_df.columns = [f'{a}_{b}' for a, b in pivot_df.columns]
        pivot_df = pivot_df.reset_index()

        pivot_df['Existing'] = pivot_df[['Existing_Affected_Medium', 'Existing_Affected_High']].bfill(axis=1).iloc[:, 0]

        x = np.arange(len(pivot_df['Threshold']))
        width = 0.3 

        viridis = cm.get_cmap('Paired')
        color_med = viridis(0.1) 
        color_med_light = viridis(0)
        color_high = viridis(0.3)  
        color_high_light = viridis(0.2)


        hatches = ['/','\\']


        plt.figure(figsize=(8,8))

        plt.rcParams['axes.linewidth'] = 2.0
        plt.rcParams["font.family"] = "Times New Roman"
        parameters = {
            'axes.labelsize': 16,
            'xtick.labelsize': 14,
            'ytick.labelsize': 14,
            'axes.titlesize': 0,
            'xtick.major.pad': 1,
            'ytick.major.pad': 0,}

        plt.rcParams.update(parameters)
        plt.bar(x, pivot_df['Existing'], width=width*2,
        facecolor='none', edgecolor='lightgrey')
        line_sizes = [3,2]
        for i, hatch_color in enumerate([color_med, color_high]):
            plt.rcParams['hatch.linewidth'] = 3-2*i
            plt.bar(x, pivot_df['Existing'], width=width*2,
                    facecolor='none',
                    hatch=hatches[i],
                    edgecolor=hatch_color,
                    linewidth=line_sizes[i],
                    label='Existing')
        plt.rcParams['hatch.linewidth'] = 3
        plt.bar(x - width/2, pivot_df['Newly_Affected_Medium'], bottom=pivot_df['Existing'], hatch='/',edgecolor=color_med,linewidth = 2,
                width=width, color=color_med_light, label='Medium Freq')
        plt.rcParams['hatch.linewidth'] = 1
        plt.bar(x + width/2, pivot_df['Newly_Affected_High'], bottom=pivot_df['Existing'], hatch='\\',edgecolor=color_high,linewidth = 2,
                width=width, color=color_high_light, label='High Freq')
        
        plt.xticks(x, pivot_df['Threshold'])
        plt.xlabel("Noise Threshold (dBA)")
        plt.ylabel(f'Number of {category} Impacted')
        plt.legend(title="")
        plt.tight_layout()
        plt.grid()


        plt.savefig(f'JournalPlots/{city}_{category}_impact_bar_hybrid.png', dpi=900)
        plt.close()
