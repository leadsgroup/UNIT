
# to read and visualize spacial data
import geopandas as gpd

# to provide basemaps
import contextily as ctx

# to give more power to your figures(plots)
import matplotlib.pyplot as plt


# In[128]:


# load a data file
# note the relative filepath. where is the file located?

la_gdf = gpd.read_file('data income la county/filtered_income_data_lacounty.geojson')
sanbernardino_gdf = gpd.read_file('data income san bernardino/acs2022_5yr_B19001_14000US06071009712.geojson')
orange_gdf = gpd.read_file('data income orange county/acs2022_5yr_B19001_14000US06059021827.geojson')
riverside_gdf = gpd.read_file('data income riverside county/acs2022_5yr_B19001_14000US06065042719.geojson')

#rows represent each census tract

# DELETING COUNTY ROWS
# the first row in the data obtained from censusreporter is for the entire county. We must delete it
# drop with index 0 (i.e. the first row)
la_gdf = la_gdf.drop([0])
sanbernardino_gdf = sanbernardino_gdf.drop([0])
orange_gdf = orange_gdf.drop([0])
riverside_gdf = riverside_gdf.drop([0])

# create a list of columns to keep
columns_to_keep = ['geoid',
                  'name',
                   'B19001001',
                   'B19001002',
                   'B19001003',
                   'B19001004',
                  'B19001005',
                  'B19001006',
                  'B19001007',
                  'B19001008',
                  'B19001009',
                   'B19001010',
                  'B19001011',
                  'B19001012',
                    'B19001013',
                    'B19001014',
                    'B19001015',
                    'B19001016',
                    'B19001017',
                  'geometry']


# redefine gdf with only columns to keep
la_gdf = la_gdf[columns_to_keep]
sanbernardino_gdf = sanbernardino_gdf[columns_to_keep]
orange_gdf = orange_gdf[columns_to_keep]
riverside_gdf = riverside_gdf[columns_to_keep]

# rename the columns
la_gdf.columns = ['Geoid',
               'Name',
               'Total',
              'Less than $10,000',
               '$10,000 to $14,999',
              '$15,000 to $19,999',
              '$20,000 to $24,999',
              '$25,000 to $29,999',
              '$30,000 to $34,999',
              '$35,000 to $39,999',
              '$40,000 to $44,999',
              '$45,000 to $49,999',
               '$50,000 to $59,999',
               '$60,000 to $74,999',
               '$75,000 to $99,999',
               '$100,000 to $124,999',
               '$125,000 to $149,999',
               '$150,000 to $199,999',
               '$200,000 or more',
              'Geometry']
sanbernardino_gdf.columns = ['Geoid',
               'Name',
               'Total',
              'Less than $10,000',
               '$10,000 to $14,999',
              '$15,000 to $19,999',
              '$20,000 to $24,999',
              '$25,000 to $29,999',
              '$30,000 to $34,999',
              '$35,000 to $39,999',
              '$40,000 to $44,999',
              '$45,000 to $49,999',
               '$50,000 to $59,999',
               '$60,000 to $74,999',
               '$75,000 to $99,999',
               '$100,000 to $124,999',
               '$125,000 to $149,999',
               '$150,000 to $199,999',
               '$200,000 or more',
              'Geometry']
orange_gdf.columns = ['Geoid',
               'Name',
               'Total',
              'Less than $10,000',
               '$10,000 to $14,999',
              '$15,000 to $19,999',
              '$20,000 to $24,999',
              '$25,000 to $29,999',
              '$30,000 to $34,999',
              '$35,000 to $39,999',
              '$40,000 to $44,999',
              '$45,000 to $49,999',
               '$50,000 to $59,999',
               '$60,000 to $74,999',
               '$75,000 to $99,999',
               '$100,000 to $124,999',
               '$125,000 to $149,999',
               '$150,000 to $199,999',
               '$200,000 or more',
              'Geometry']
riverside_gdf.columns = ['Geoid',
               'Name',
               'Total',
              'Less than $10,000',
               '$10,000 to $14,999',
              '$15,000 to $19,999',
              '$20,000 to $24,999',
              '$25,000 to $29,999',
              '$30,000 to $34,999',
              '$35,000 to $39,999',
              '$40,000 to $44,999',
              '$45,000 to $49,999',
               '$50,000 to $59,999',
               '$60,000 to $74,999',
               '$75,000 to $99,999',
               '$100,000 to $124,999',
               '$125,000 to $149,999',
               '$150,000 to $199,999',
               '$200,000 or more',
              'Geometry']

# SORTING

gdf_sorted1 = la_gdf.sort_values(by = 'Total', ascending = False)
gdf_sorted2 = sanbernardino_gdf.sort_values(by = 'Total', ascending = False)
gdf_sorted3 = orange_gdf.sort_values(by = 'Total', ascending = False)
gdf_sorted4 = riverside_gdf.sort_values(by = 'Total', ascending = False)

# Create subplots with shared axes
fig, ax = plt.subplots(figsize=(10, 10))

# Plot the first set of data
gdf_sorted1 = gdf_sorted1.set_geometry('Geometry')
gdf_sorted1.head(10).plot(ax=ax, color='blue', label='gdf_sorted1')

# Plot the second set of data on the same axes
gdf_sorted2 = gdf_sorted2.set_geometry('Geometry')
gdf_sorted2.head(10).plot(ax=ax, color='red', label='gdf_sorted2')

# Plot the third set of data on the same axes
gdf_sorted3 = gdf_sorted3.set_geometry('Geometry')
gdf_sorted3.head(10).plot(ax=ax, color='red', label='gdf_sorted3')

# Plot the fourth set of data on the same axes
gdf_sorted4 = gdf_sorted4.set_geometry('Geometry')
gdf_sorted4.head(10).plot(ax=ax, color='red', label='gdf_sorted4')

# Set plot title and legend
ax.set_title('Top 10 Most Populated Tracts')
ax.legend()

# Show the plot
plt.show()



# FILTERING AND SUBSETTING DATA
# Assuming gdf is your GeoDataFrame containing the columns you mentioned
columns_to_sum1 = ['Less than $10,000', '$10,000 to $14,999', '$15,000 to $19,999',
                  '$20,000 to $24,999', '$25,000 to $29,999', '$30,000 to $34,999',
                  '$35,000 to $39,999', '$40,000 to $44,999', '$45,000 to $49,999']

# Sum the specified columns and create a new column called 'Total'
gdf_sorted1['TotL'] = gdf_sorted1[columns_to_sum1].sum(axis=1)

# Plot the GeoDataFrame using the 'Total' column
gdf_sorted1.plot(figsize=(12, 10), column='TotL', legend=True)
plt.title('Total Income of Less than $50,000')
plt.show()

# Sum the specified columns and create a new column called 'Total'
gdf_sorted2['TotL'] = gdf_sorted2[columns_to_sum1].sum(axis=1)

# Plot the GeoDataFrame using the 'Total' column
gdf_sorted2.plot(figsize=(12, 10), column='TotL', legend=True)
plt.title('Total Income of Less than $50,000')
plt.show()

# Sum the specified columns and create a new column called 'Total'
gdf_sorted3['TotL'] = gdf_sorted3[columns_to_sum1].sum(axis=1)

# Plot the GeoDataFrame using the 'Total' column
gdf_sorted3.plot(figsize=(12, 10), column='TotL', legend=True)
plt.title('Total Income of Less than $50,000')
plt.show()

# Sum the specified columns and create a new column called 'Total'
gdf_sorted4['TotL'] = gdf_sorted4[columns_to_sum1].sum(axis=1)

# Plot the GeoDataFrame using the 'Total' column
gdf_sorted4.plot(figsize=(12, 10), column='TotL', legend=True)
plt.title('Total Income of Less than $50,000')
plt.show()


# Create subplots with shared axes
fig, ax = plt.subplots(figsize=(12, 10))

# Sum the specified columns and create a new column called 'Total' for gdf_sorted1
gdf_sorted1['TotL'] = gdf_sorted1[columns_to_sum1].sum(axis=1)

# Plot the GeoDataFrame for gdf_sorted1 using the 'Total' column
gdf_sorted1.plot(ax=ax, column='TotL', legend=True, cmap='Reds')

# Sum the specified columns and create a new column called 'Total' for gdf_sorted2
gdf_sorted2['TotL'] = gdf_sorted2[columns_to_sum1].sum(axis=1)

# Plot the GeoDataFrame for gdf_sorted2 using the 'Total' column
gdf_sorted2.plot(ax=ax, column='TotL', legend=True, cmap='Greens')

# Sum the specified columns and create a new column called 'Total' for gdf_sorted3
gdf_sorted3['TotL'] = gdf_sorted3[columns_to_sum1].sum(axis=1)

# Plot the GeoDataFrame for gdf_sorted3 using the 'Total' column
gdf_sorted3.plot(ax=ax, column='TotL', legend=True, cmap='Blues')

# Set plot title
plt.title('Total Income of Less than $50,000')

# Show the plot
plt.show()

# Determine the maximum value of 'TotL' across all GeoDataFrames
max_value = max(gdf_sorted1['TotL'].max(), gdf_sorted2['TotL'].max(), gdf_sorted3['TotL'].max())

# Create subplots with shared axes
fig, ax = plt.subplots(figsize=(12, 10))

# Sum the specified columns and create a new column called 'TotL' for gdf_sorted1
gdf_sorted1['TotL'] = gdf_sorted1[columns_to_sum1].sum(axis=1)

# Plot the GeoDataFrame for gdf_sorted1 using the 'Total' column
gdf_sorted1.plot(ax=ax, column='TotL', legend=True, cmap='Reds', vmin=0, vmax=max_value)

# Sum the specified columns and create a new column called 'TotL' for gdf_sorted2
gdf_sorted2['TotL'] = gdf_sorted2[columns_to_sum1].sum(axis=1)

# Plot the GeoDataFrame for gdf_sorted2 using the 'Total' column
gdf_sorted2.plot(ax=ax, column='TotL', legend=True, cmap='Reds', vmin=0, vmax=max_value)

# Sum the specified columns and create a new column called 'TotL' for gdf_sorted3
gdf_sorted3['TotL'] = gdf_sorted3[columns_to_sum1].sum(axis=1)

# Plot the GeoDataFrame for gdf_sorted3 using the 'Total' column
gdf_sorted3.plot(ax=ax, column='TotL', legend=True, cmap='Reds', vmin=0, vmax=max_value)

# Set plot title
plt.title('Total Income of Less than $50,000')

# Show the plot
plt.show()


# In[144]:


import pandas as pd
import geopandas as gpd

# Assuming gdf_sorted1, gdf_sorted2, and gdf_sorted3 are your GeoDataFrames

# Concatenate the three GeoDataFrames into one
combined_gdf = pd.concat([gdf_sorted1, gdf_sorted2, gdf_sorted3, gdf_sorted4])

# Plot the combined GeoDataFrame
combined_gdf.plot(figsize=(12, 10), column='TotL', legend=True, cmap='Reds')

# Set plot title
plt.title('Total Income of Less than $50,000')

# Show the plot
plt.show()


# Save the combined GeoDataFrame to a file
combined_gdf.to_file('3combined_data_income.geojson', driver='GeoJSON')


# Assuming gdf is your GeoDataFrame containing the columns you mentioned
columns_to_sum2 = ['$50,000 to $59,999',
 '$60,000 to $74,999',
 '$75,000 to $99,999',
 '$100,000 to $124,999',
 '$125,000 to $149,999',
 '$150,000 to $199,999',
 '$200,000 or more']

# Sum the specified columns and create a new column called 'Total'
combined_gdf['TotH'] = combined_gdf[columns_to_sum2].sum(axis=1)

# create 1 x 2 subplots
fig, axs = plt.subplots(1, 2, figsize = (15, 12))

# name each subplot
ax1, ax2 = axs

# regular count map on the left
combined_gdf.plot(column = 'TotL',
         cmap = 'plasma',
         k = 5,
         edgecolor = 'white',
         linewidth = 0.0,
         alpha = 0.75,
         ax = ax1,
         legend = True)
ax1.axis("off")
ax1.set_title("Population with Total Income Less Than $50,000")

# spatial log map on the right
combined_gdf.plot(column="TotH",
         cmap='plasma',
         k=5,
         edgecolor='white',
         linewidth=0.0,
         alpha=0.75,
         ax=ax2,
         legend=True)
ax2.axis("off")
ax2.set_title("Population with Total Income $50,000 or More")

plt.show()


