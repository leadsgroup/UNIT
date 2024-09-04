# SCHOOLS
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
from matplotlib.colors import Normalize
from shapely.geometry import Point

# load data for LA county shapefile and schools
boundary_gdf = gpd.read_file('data la county edited/Edited_CensusData_LACounty_filtered.geojson')
schools_gdf = gpd.read_file('various coords/Schools_Colleges_and_Universities_-4260208272874444542.geojson')

# extract the coordinates of the schools
coords = np.vstack([schools_gdf.geometry.x, schools_gdf.geometry.y])

# do the gaussian kernel density estimation (KDE) (this is to measure the concentration of the schools on the map)
kde = gaussian_kde(coords)
density = kde(coords)

# create a grid over the map to calculate the KDE on the entire area
xmin, ymin, xmax, ymax = boundary_gdf.total_bounds
x = np.linspace(xmin, xmax, 100)
y = np.linspace(ymin, ymax, 100)
X, Y = np.meshgrid(x, y)
xy = np.vstack([X.ravel(), Y.ravel()])

# evaluate KDE on the grid
Z = np.reshape(kde(xy).T, X.shape)

# create a mask for the grid points that are inside the county boundary
mask = np.zeros(Z.shape, dtype=bool)

# iterate over grid points to check if within county boundary
for i in range(Z.shape[0]):
    for j in range(Z.shape[1]):
        point = Point(X[i, j], Y[i, j])
        if boundary_gdf.geometry.contains(point).any():
            mask[i, j] = True

# mask areas outside county boundary
Z_masked = np.ma.masked_where(~mask, Z)

# create plot
fig, ax = plt.subplots(figsize=(12, 12))

# plot LA County boundaries
boundary_gdf.plot(ax=ax, color='lightgrey', edgecolor='black')

# overlaying contour plot with masked data
contour = ax.contourf(X, Y, Z_masked, levels=20, cmap='viridis', alpha=0.7, norm=Normalize(vmin=Z.min(), vmax=Z.max()))
plt.colorbar(contour, ax=ax, label='Density')

# labeling plot and showing
ax.set_title('LA County Schools Density Contour')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_aspect('equal')

plt.show()