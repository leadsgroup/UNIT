# NOTE:
# this code works for editing GeoJSON files. if intending to edit a different file type, it must be converted to
# GeoJSON first

# additonally, the default of this code is to edit 5-year tract census data for counties and save
# the edited data to your coding repository
# if intending to edit a different type of census data, must alter the code accordingly

# to read and visualize spacial data
import geopandas as gpd

# to provide basemaps
import contextily as ctx

# to give more power to your figures(plots)
import matplotlib.pyplot as plt


# Load the data file
gdf = gpd.read_file('data/acs2022_5yr_B03002_14000US06037602301.geojson')

# Delete the county rows
gdf = gdf.drop([0])

# Define columns to keep
columns_to_keep = ['geoid',
                   'name',
                   'B03002001',
                   'B03002002',
                   'B03002003',
                   'B03002004',
                   'B03002005',
                   'B03002006',
                   'B03002007',
                   'B03002008',
                   'B03002009',
                   'B03002012',
                   'geometry']

# Redefine gdf with only columns to keep
gdf = gdf[columns_to_keep]

# Sorting
gdf_sorted = gdf.sort_values(by='B03002001', ascending=False)

# Filtering and subsetting data
gdf_no_pop = gdf_sorted[gdf_sorted['B03002001'] == 0]

# Normalizing the data
gdf_sorted = gdf_sorted.copy()
gdf_sorted['Percent Non Hispanic White alone'] = gdf_sorted['B03002003'] / gdf_sorted['B03002001'] * 100
gdf_sorted['Percent Non Hispanic Black or African American alone'] = gdf_sorted['B03002004'] / gdf_sorted['B03002001'] * 100
gdf_sorted['Percent Non Hispanic American Indian and Alaska Native alone'] = gdf_sorted['B03002005'] / gdf_sorted['B03002001'] * 100
gdf_sorted['Percent Non Hispanic Asian alone'] = gdf_sorted['B03002005'] / gdf_sorted['B03002006'] * 100
gdf_sorted['Percent Non Hispanic Native Hawaiian and Other Pacific Islander alone'] = gdf_sorted['B03002007'] / gdf_sorted['B03002001'] * 100
gdf_sorted['Percent Non Hispanic Some Other Race alone'] = gdf_sorted['B03002008'] / gdf_sorted['B03002001'] * 100
gdf_sorted['Percent Non Hispanic Two or More Races'] = gdf_sorted['B03002009'] / gdf_sorted['B03002001'] * 100
gdf_sorted['Percent Hispanic or Latino'] = gdf_sorted['B03002012'] / gdf_sorted['B03002001'] * 100

# Save the edited data GeoDataFrame to a GeoJSON file
gdf_sorted.to_file('Edited_CensusData_LACounty.geojson', driver='GeoJSON')

