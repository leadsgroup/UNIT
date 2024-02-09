# UNIT
Urban Noise Impact Tool

This code is utilized to IMPORT census and noise data, EDIT it, and MAP the two data sets

FIRST, the census data must be imported and run through the Pre-Processing Census Data.py
The Pre-Processing Census Data.py takes in GeoJSON files for 5-year Tract Census Data and exports the edited data to your current repository
to be used for mapping

Call the edited census data (in GeoJSON format) and the noise data (in csv) in NoiseImpactMapping.py to display them separately in the form of a 2D map
