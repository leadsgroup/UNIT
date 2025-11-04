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

- Process different noise data sources (DOT / ambient sensors / research leads) and join them to census tracts (GeoJSON).
- Compute per-tract summary statistics (mean noise values, counts of points above thresholds, tract area).
- Identify unique research noise points that are not represented by existing DOT clusters (DBSCAN clustering + convex hulls).
- Compute how many sensitive structures (schools, hospitals, places of worship) fall inside existing and newly detected noise hulls.
- Estimate single-unit households impacted using tract area, microphone density, and census household counts. Compute an approximate economic cost per household.
- Produce high-resolution publication-ready plots (hulls, contour maps, barplots, line plots) saved to `JournalPlots/`, `LA_Plots/`, `DFW_Plots/`.

## Repository layout (relevant files)

- `UNIT.py` — example runner that demonstrates full workflow for LA and DFW (reads raw CSVs, reads geojson, saves results and plots).
- `NoisePreProcess.py` — functions:
	- `process_noise_impact` / `process_DOT_noise` — join point noise data to census tracts and save GeoJSON/CSV
	- `sensitive_structs` — count sensitive structure points per tract
	- `process_unique_research_noise` — create tract-level noise_count from a GeoDataFrame of unique research noise
	- `difference_noise_pts` — remove research points that fall inside DOT clusters (DBSCAN + convex hull) returning unique research points
	- `struct_in_contours` — detect structures inside existing DOT hulls and newly detected hulls and produce a summary DataFrame (also saves a plot)
- `Plots.py` — plotting and summary helpers: `compute_single_households`, `compute_impacted`, `plot_homes_impacted`, `hull_plots`, `struct_stats_barplot`, etc.
- `Final_*_Data/`, `DFWRawData/`, `LARawDat/` — data directories (CSV/GeoJSON) used by `UNIT.py` in examples.

## Expected inputs

- Census tracts: GeoJSON (polygons) with tract geometries and census variables (household counts used by plotting/impact functions). Example: `Final_DFW_Data/DFW_53_High_Noise.geojson` and raw `DFWRawData/DFWHousing.geojson`.
- Noise files (CSV): DOT sensor CSVs with `Longitude`, `Latitude`, `value` (or `L_dn`), and research noise CSVs with `Longitude`, `Latitude`, `L_dn`, etc. Example files are in `DFWRawData/` and `LARawDat/`.
- Sensitive-structure CSVs: CSVs with `Longitude`, `Latitude` and other attributes for schools, hospitals, churches. Examples in `DFWRawData/` and `LARawDat/`.

If your files use different column names, update the helper calls or adapt the small wrappers in the scripts.

## Installation

Recommended: create a Python virtual environment and install required packages.

```bash
# macOS / zsh example
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install pandas geopandas shapely scikit-learn matplotlib seaborn numpy
```

Note: `geopandas` may require system dependencies (GDAL, Fiona). Use conda if you prefer:

```bash
conda create -n unit-env python=3.10 geopandas pandas scikit-learn matplotlib seaborn numpy -y
conda activate unit-env
```

## Quick usage

1) Run the example orchestration (requires the raw data folders present in the repo):

```bash
python UNIT.py
```

This will:
- create output folders `Final_LA_Data`, `Final_DFW_Data`, `LA_Plots`, `DFW_Plots` (as used in the script)
- read noise CSVs and sensitive-structure CSVs from the `*RawData/` directories
- compute impacted households and save plots to `*_Plots/` and `JournalPlots/`

2) Use module functions directly from a Python session:

```python
from NoisePreProcess import difference_noise_pts, struct_in_contours, process_DOT_noise
from Plots import compute_single_households, compute_impacted, plot_homes_impacted

# Example: find research points unique from DOT clusters
unique_pts = difference_noise_pts('DFWRawData/TX_Aviation_Modes.csv', 'DFWRawData/Cumulative_Nov_High_Freq_TR_DFW_1000ft.csv', threshold=60)

# Example: summarize structures in contours
summary_df = struct_in_contours(
		geojson='DFWRawData/DFWHousing.geojson',
		dot_noise_file='DFWRawData/TX_Aviation_Modes.csv',
		leads_noise_file='DFWRawData/Cumulative_Nov_High_Freq_TR_DFW_1000ft.csv',
		sens_struct_list=[pd.read_csv('DFWRawData/Texas Schools.csv'), pd.read_csv('DFWRawData/Churches.csv'), pd.read_csv('DFWRawData/Hospitals.csv')],
		city='DFW',
		p_bounds=Polygon([(-97.3, 32.6), (-96.5, 32.6), (-96.5, 33.3), (-97.3, 33.3)]),
		threshold=60,
		frequency='High')

```

## Output files

- CSV summaries per tract (saved by functions that include `to_csv` calls) and GeoJSON outputs for mapped results.
- Plots saved to `JournalPlots/`, `{City}_Plots/`, and other folders created by `UNIT.py`.

## Notes, assumptions and edge cases

- The scripts assume `Longitude`, `Latitude` column names exist and sometimes subtract 360 from longitude for files that use 0–360 longitude convention. If your data uses -180..180 longitudes, adjust as needed.
- DBSCAN parameters (eps, min_samples) are set as defaults in the helper functions and can be tuned for different spatial resolutions.
- Microphone density (used to convert tract area to microphone counts) is passed as a city constant in `UNIT.py`. Adjust per your sampling design.
- Many functions expect EPSG:4326; when joining GeoDataFrames, the code attempts to match CRSs where required. Verify CRS consistency for best results.

## Next steps / suggestions

- Add a `requirements.txt` or `environment.yml` for reproducible installs.
- Provide a small sample dataset and a minimal example notebook demonstrating the full pipeline on a tiny area (makes it easy for reviewers).
- Add unit tests for data-shape assumptions (e.g., expected columns) and a CI workflow to check import and simple code paths.

## License

Add your license text here (e.g., MIT, Apache-2.0) or a short note if this is for research use only.

## Contact

For questions about the code or datasets, mention your contact details or project webpage.
