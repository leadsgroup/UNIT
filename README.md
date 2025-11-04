# UNIT — Urban Noise Impact Tool

This repository contains code to process, compare, and visualize urban noise data together with census / sensitive-structure datasets. It helps
- aggregate and join noise measurements to census tracts
- detect new or unique noise hotspots compared to baseline (DOT) noise measurements
- estimate impacted households and approximate economic cost
- visualize noise contours, hulls, and sensitive-structure impacts

The implementation centers on three modules:
- `NoisePreProcess.py` — geospatial processing and spatial-join utilities to aggregate noise to census tracts and calculate per-tract noise counts
- `Plots.py` — plotting helpers for hull visualizations, impact barplots and time/threshold-series plots
- `UNIT.py` — orchestration script that ties the processing and plotting together for example cities (LA, DFW)

## Key capabilities

- Process different noise data sources and join them to census tracts (GeoJSON).
- Compute per-tract summary statistics (mean noise values, counts of points above thresholds, tract area).
- Identify unique research noise points that are not represented by existing DOT clusters (DBSCAN clustering + convex hulls).
- Compute how many sensitive structures (schools, hospitals, places of worship) fall inside existing and newly detected noise hulls.
- Estimate single-unit households impacted using tract area, microphone density, and census household counts. Compute an approximate economic cost per household.

## Repository layout (relevant files)

- `UNIT.py` — example runner that demonstrates full workflow for LA and DFW (reads raw CSVs, reads geojson, saves results and plots).
- `NoisePreProcess.py` — functions:
	- `process_unique_research_noise` — create tract-level noise_count from a GeoDataFrame of unique research noise
	- `difference_noise_pts` — returns unique noise points comapred to existing datasets
	- `struct_in_contours` — detect structures inside existing noise hulls and newly detected hulls and produce a summary DataFrame
- `Plots.py` — plotting and summary helpers: `compute_single_households`, `compute_impacted`, `plot_homes_impacted`, `hull_plots`, `struct_stats_barplot`, etc.

## Expected inputs

- Census tracts: GeoJSON (polygons) with tract geometries and census variables (household counts used by plotting/impact functions). Example: `Final_DFW_Data/DFW_53_High_Noise.geojson` and raw `DFWRawData/DFWHousing.geojson`.
- Noise files (CSV): CSVs with `Longitude`, `Latitude`, and research noise CSVs with `Longitude`, `Latitude`, `L_dn`, etc. Example files are in `DFWRawData/` and `LARawDat/`.
- Sensitive-structure CSVs: CSVs with `Longitude`, `Latitude` and other attributes for schools, hospitals, churches.

An example dataset can be found here: https://drive.google.com/drive/folders/1iSdyvAMdHfDRQ2PiccRgtiSDFWTrRzvF?usp=drive_link 

## Output files

- CSV summaries per tract (saved by functions that include `to_csv` calls) and GeoJSON outputs for mapped results.
- Plots saved to `JournalPlots/`, `{City}_Plots/`, and other folders created by `UNIT.py`.

