# Documentation for Mosaik Data Analysis Pipeline


This document provides a comprehensive guide to the pipeline developed for processing, analyzing, and visualizing Mosaik data and Shrid level Satellite images. Each step is detailed with explanations of its purpose and functionality.

## 1. Importing Libraries

```python
import pandas as pd
import numpy as np
import os
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from shapely.geometry import Point, Polygon
import geopandas as gpd
import warnings
warnings.filterwarnings('ignore')
```

### Purpose:
- **Pandas**: For handling tabular data.
- **NumPy**: For numerical computations.
- **OS**: To manage file paths and directories.
- **Scikit-learn**: For Principal Component Analysis (PCA) to reduce dimensionality.
- **Matplotlib and Seaborn**: For visualization.
- **Shapely and GeoPandas**: For handling spatial data (polygons, points, etc.).
- **Warnings**: To suppress irrelevant warnings for smoother output.

### Why:
These libraries form the foundation of the data analysis workflow, enabling us to efficiently handle, manipulate, and visualize the data.



## 2. Loading Data

```python
# Load Mosaik data
csv_file = "path_to_mosaik_data.csv"
data1 = pd.read_csv(csv_file)

# Load Shrid Polygon data
csv_file = "path_to_polygon_data.csv"
data2 = pd.read_csv(csv_file)
```

### Purpose:
- Load two separate datasets: one containing Mosaik features and another with Shrid polygon coordinates.

### Why:
We need both datasets to merge and analyze data at the Shrid level. Mosaik data contains features for analysis, while polygon data provides spatial information.



## 3. Merging Datasets

```python
# Merge datasets on 'shrid'
data = pd.merge(data1, data2, on='shrid', how='inner')

# Save the merged dataset
output_file = 'merged_dataset.csv'
data.to_csv(output_file, index=False)
print(f"Merged data saved to {output_file}")
```

### Purpose:
- Merge the Mosaik data and polygon data on the common column `shrid`.
- Save the merged dataset for future use.

### Why:
Combining these datasets allows us to perform a unified analysis linking spatial data with Mosaik features.



## 4. Renaming Mosaik Feature Columns

```python
csv_file = "path_to_merged_data.csv"
data = pd.read_csv(csv_file)
for i, col in enumerate(data.columns[4:], start=1):
    data.rename(columns={col: f"Mosaik_{i}"}, inplace=True)
data.to_csv("renamed_features.csv", index=False)
data.head(2)
```

### Purpose:
- Rename Mosaik feature columns to a standard format (e.g., `Mosaik_1`, `Mosaik_2`).
- Save the updated dataset.

### Why:
Renaming columns ensures clarity and consistency when working with Mosaik features.



## 5. Generating Satellite Images for Shrids

### Code Highlights:
- **Converting Polygon Data to GeoDataFrame:**
  ```python
  def parse_polygon(row):
      coords = eval(row['polygon_coordinates'])
      return Polygon(coords)
  data['geometry'] = data.apply(parse_polygon, axis=1)
  gdf = gpd.GeoDataFrame(data, geometry='geometry')
  ```

- **Filtering Urban Areas:**
  ```python
  def is_urban(polygon):
      centroid = polygon.centroid
      return (centroid.x > urban_threshold_lon) and (centroid.y > urban_threshold_lat)
  gdf['is_urban'] = gdf['geometry'].apply(is_urban)
  urban_gdf = gdf[gdf['is_urban']]
  ```

- **Saving Satellite Images:**
  ```python
  def plot_and_save_shrid(row, zoom_level=15):
      ...
      ctx.add_basemap(ax, crs=gdf.crs.to_string(), source=ctx.providers.Esri.WorldImagery, attribution=False, zoom=zoom_level)
      plt.savefig(output_path, dpi=300, bbox_inches='tight')
  ```

### Purpose:
- Convert polygon coordinates to spatial data.
- Filter polygons representing urban areas.
- Save satellite imagery for each urban Shrid polygon.

### Why:
Visualizing polygons with satellite imagery provides spatial context for analysis, enabling comparisons between urban and rural regions.



## 6. Generating Heatmaps

### Code Highlights:
- **PCA for Dimensionality Reduction:**
  ```python
  mosaik_features = data.iloc[:, 4:]
  pca = PCA(n_components=1)
  data['PCA_1'] = pca.fit_transform(mosaik_features)
  ```

- **Creating Heatmap Data:**
  ```python
  heatmap_data = [[row['Lat_x'], row['Lon_x'], row['PCA_1']] for idx, row in selected_data.iterrows() if selected_polygon.contains(Point(row['Lon_x'], row['Lat_x']))]
  ```

- **Saving Heatmap:**
  ```python
  HeatMap(heatmap_data).add_to(m)
  m.save(f"heatmap_{shrid_id}.html")
  ```

### Purpose:
- Reduce Mosaik features to a single component for visualization.
- Generate heatmaps showing feature intensity within polygons.
- Save heatmaps as interactive HTML files.

### Why:
Heatmaps provide an intuitive way to visualize spatial intensity, aiding decision-making and further analysis.



## Summary
This pipeline efficiently combines, processes, and visualizes spatial and feature data at the Shrid level. The steps ensure that both technical users and analysts can gain insights into Mosaik data, urbanization patterns, and feature distributions. The output files and visualizations are structured for immediate use in reports or further processing.