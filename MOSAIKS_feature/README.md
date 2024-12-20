## Purpose of Package ##
This is a Python Library generated to replicate the steps done by the research in `Program Evaluation with Remotely Sensed Outcomes` by Ashesh Rambachan, Rahul Singh, and Davide Viviano†. 

### NOTE: Before running code, make sure to install the libraries and versions required in `requirements.txt`

## Package Overview ##
```
├── src/MOSAIKS_feature/
    ├── analysis/
    │   ├── __init__.py
    │   ├── img_generation_heatmap.py   
    |   ├── Satellite_Image_Generation and Mosaiks_Heat_Map-Documentation_Final.md
    ├── extract_features/
    │   ├── __init__.py
    │   ├── aggregate_features.py
    │   ├── granular_all_coords.py
    │   ├── granular_coords_inside_polygon.py
    │   ├── strategy_two.py
    ├── testing/
    │   ├── __init__.py
    │   ├── aggregate_features_functional.py
    │   ├── granular_coords_functional.py
    │   ├── strategy_two_functional.py   
    ├── __init__.py
    ├── misc.py
    ├── requirements.txt
├── tests/
```
### Analysis
`img_generation_heatmap.py`: Processes, analyzes, and visualizes Mosaik data and SHRID level Satellite images
`Satellite_Image_Generation and Mosaiks_Heat_Map-Documentation_Final.md`: Documentation for how analysis pipeline

### Extract Features
`aggregate_features.py`: 
- Purpose: This script averages the MOSAIKS feature data for each coordinate to create a summarized dataset. 
- Steps:
    - Run aggregate_features.py on the downloaded MOSAIKS result files
    - The script will compute the average of each feature across the files for each coordinate
- Output: A final CSV file with the averaged features for each coordinate point, ready for further analysis

`granular_all_coords.py` and `granular_coords_inside_polygon.py`: 
- Purpose: This script processes a CSV of polygon coordinates, breaking down each polygon into more granular coordinate points. The former generates all coordinates from the mininmum and maximum lon/lat, whereas the latter filters for coordinates that are only inside the polygoon coordinate. 
- Steps:
    - Run v3.py on the original CSV of polygon coordinates
    - The script will divide the coordinates into multiple output files, each containing no more than 100,000 rows, to meet the MOSAIKS input limitation
- Output: Several CSV files with a maximum of 100,000 rows each, containing the granular versions of the polygon coordinates

`strategy_two.py`:
- Purpose: This method simplifies feature extraction by using the centroid (central longitude and latitude) of each polygon rather than a granular breakdown, addressing the requirement to get one set of features per grid.
- Steps:
    - Prepare a CSV file containing the centroid longitude and latitude for each polygon.
    - Upload the centroid CSV file into the MOSAIKS file query system.
    - Execute the query to gather features for the centroid of each polygon.
    - Download the resulting feature files from MOSAIKS once the query completes.
- Output: A MOSAIKS result file containing features for the centroid coordinates of each polygon.

### `misc.py`: 
- Various python functions for additional csv functionalities such as removing duplicates, merging files, counting distinct rows, and grabing a subset of a csv

### tests/
- Test files for aggregate_features_functional.py, granular_coords_functional.py, and strategy_two_functional.py

### Testing
These code files replicate the functionality of those in the `Extract Features` directory, but have been refactored into more modular, function-based components. This approach enables testing within a separate tests folder, external to the MOSAIKS_features directory.

## Replication Steps ##
### MOSAIKS Feature Extraction Guide

This guide provides step-by-step instructions for generating granular coordinates, querying MOSAIKS for features, and aggregating the results.

---

#### Step 1: Generate Granular Coordinates

To begin, generate granular coordinates using an input CSV file with the following required columns:

- `Unnamed: 0`
- `shrid2`
- `polygon_coordinates`
- `min_lat`
- `max_lat`
- `min_lon`
- `max_lon`
- `centroid_lon`
- `centroid_lat`

Depending on your requirements, choose one of the following methods:

##### Option 1: Generate Granular Coordinates Within the Polygon

If you want to generate only the granular coordinates that fit strictly within the polygon, use the following code:

```python
from MOSAIKS_feature.extract_features.granular_coords_inside_polygon import granular
file = ""
granular(file)
```

##### Option 2: Generate General Granular Coordinates Using Min/Max Bounds

To generate granular coordinates using only the minimum and maximum latitude and longitude values, use the following code:
```python
from MOSAIKS_feature.extract_features.granular_all_coords import granular_all_coords
file = ""
granular_all_coords(file)
```

##### Option 3: Generate Coordinates by Averaging the Center Point of the Polygon

If you want to collect coordinates by averaging the center point of each polygon, use the following code:
```python
from MOSAIKS_feature.extract_features.strategy_two import process_shrid_bounding_boxes
file = ""
process_shrid_bounding_boxes(file)
```

#### Step 2: Query Features Using MOSAIKS

- **Purpose:** Leverage the granular coordinates generated in Step 1 to query MOSAIKS for features associated with each coordinate.

- **Instructions:**

	1.	Upload the CSV files created in Step 1 to the MOSAIKS file query system.
	2.	Execute the query to generate features for each coordinate point.
	3.	Once the queries are complete, download the resulting files.

- **Output:** You will receive a set of CSV files from MOSAIKS, each containing features associated with the granular coordinates.

#### Step 3: Aggregate the Results

Combine the downloaded results from MOSAIKS into a unified dataset.

```python
from MOSAIKS_feature.extract_features.aggregate_features import aggregate
file_path = ""
aggregate(file_path)
```
**Note:**
    - Ensure that file_path points to the files downloaded in Step 2.
    - Important: Do not use the same file path as the one used in Step 1.

### MOSAIKS Analysis

Further analysis can be done via the files in `analysis` directory. Be sure to import the functions similar to how it is demoed above. 