import pandas as pd
import os
import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as ctx
import warnings
import folium
from folium.plugins import HeatMap
from shapely.geometry import Point, Polygon
from sklearn.decomposition import PCA

warnings.filterwarnings('ignore')

def load_data(mosaik_file: str, polygon_file: str):
    """
    Load Mosaik and polygon data from CSV files.

    Parameters
    ----------
    mosaik_file : str
        Path to the Mosaik CSV file.
    polygon_file : str
        Path to the polygon CSV file.

    Returns
    -------
    tuple (pd.DataFrame, pd.DataFrame)
        Loaded dataframes: (mosaik_data, polygon_data)
    """
    try:
        mosaik_data = pd.read_csv(mosaik_file)
        polygon_data = pd.read_csv(polygon_file)
        return mosaik_data, polygon_data
    except Exception as e:
        raise IOError(f"Error loading files: {e}")


def merge_data(mosaik_data: pd.DataFrame, 
               polygon_data: pd.DataFrame, 
               output_file: str = None) -> pd.DataFrame:
    """
    Merge Mosaik and polygon data on 'shrid'.

    Parameters
    ----------
    mosaik_data : pd.DataFrame
        DataFrame containing Mosaik data.
    polygon_data : pd.DataFrame
        DataFrame containing polygon data.
    output_file : str, optional
        If provided, save the merged DataFrame to the given CSV file path.

    Returns
    -------
    pd.DataFrame
        The merged DataFrame.
    """
    merged_data = pd.merge(mosaik_data, polygon_data, on='shrid', how='inner')
    if output_file:
        merged_data.to_csv(output_file, index=False)
    return merged_data

def rename_mosaik_features(data: pd.DataFrame, 
                           start_col_index: int = 4,
                           prefix: str = "Mosaik_", 
                           output_file: str = None) -> pd.DataFrame:
    """
    Rename Mosaik features starting from a certain column index.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame with features to be renamed.
    start_col_index : int, optional
        The column index from where the renaming of columns should start.
    prefix : str, optional
        The prefix for renamed columns.
    output_file : str, optional
        If provided, save the renamed DataFrame to the given CSV file path.

    Returns
    -------
    pd.DataFrame
        DataFrame with renamed features.
    """
    for i, col in enumerate(data.columns[start_col_index:], start=1):
        data.rename(columns={col: f"{prefix}{i}"}, inplace=True)
    if output_file:
        data.to_csv(output_file, index=False)
    return data

def save_shrid_images(data: pd.DataFrame, 
                      output_dir: str, 
                      urban_threshold_lat: float = 10.0,
                      urban_threshold_lon: float = 75.0,
                      zoom_level: int = 15):
    """
    Save images of shrids (polygons) that meet an 'urban' threshold criterion.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing 'shrid2' and 'polygon_coordinates' columns.
    output_dir : str
        Directory to save the output images.
    urban_threshold_lat : float, optional
        Latitude threshold for defining urban shrids.
    urban_threshold_lon : float, optional
        Longitude threshold for defining urban shrids.
    zoom_level : int, optional
        Zoom level for the basemap.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Ensure polygon_coordinates can be parsed into Polygon objects
    data['geometry'] = data.apply(lambda row: Polygon(eval(row['polygon_coordinates'])), axis=1)
    gdf = gpd.GeoDataFrame(data, geometry='geometry', crs="EPSG:4326")

    # Determine urban shrids based on centroid
    gdf['is_urban'] = gdf['geometry'].apply(
        lambda poly: poly.centroid.y > urban_threshold_lat and poly.centroid.x > urban_threshold_lon
    )
    urban_gdf = gdf[gdf['is_urban']]

    def plot_shrid(shrid_row):
        fig, ax = plt.subplots(figsize=(10, 10))
        gdf[gdf['shrid2'] == shrid_row['shrid2']].plot(ax=ax, facecolor="none", edgecolor="blue", linewidth=2)
        ctx.add_basemap(ax, crs=gdf.crs.to_string(), source=ctx.providers.Esri.WorldImagery, attribution=False, zoom=zoom_level)
        ax.axis("off")
        sanitized_shrid = str(shrid_row['shrid2']).replace('-', '_')
        plt.savefig(os.path.join(output_dir, f"shrid_{sanitized_shrid}.png"), dpi=300, bbox_inches='tight')
        plt.close(fig)

    for _, row in urban_gdf.iterrows():
        plot_shrid(row)

def generate_heatmaps(data: pd.DataFrame,
                      output_folder: str,
                      lat_col: str = 'Lat_x', 
                      lon_col: str = 'Lon_x',
                      polygon_col: str = 'polygon_coordinates', 
                      feature_start_idx: int = 4,
                      zoom_start: int = 15):
    """
    Generate interactive HTML heatmaps for each unique shrid in the data.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing polygon coordinates and mosaik features.
    output_folder : str
        Directory to save the HTML heatmap files.
    lat_col : str, optional
        Column name for latitude.
    lon_col : str, optional
        Column name for longitude.
    polygon_col : str, optional
        Column name containing polygon coordinate strings.
    feature_start_idx : int, optional
        Index from which Mosaik features start.
    zoom_start : int, optional
        Initial zoom level for the folium map.
    """
    os.makedirs(output_folder, exist_ok=True)

    # Convert polygon coordinates to geometry
    data['geometry'] = data[polygon_col].apply(lambda coords: Polygon(eval(coords)))
    gdf = gpd.GeoDataFrame(data, geometry="geometry", crs="EPSG:4326")

    # Extract Mosaik features for PCA
    mosaik_features = data.iloc[:, feature_start_idx:]
    pca = PCA(n_components=1)
    data['PCA_1'] = pca.fit_transform(mosaik_features)

    # Generate heatmaps for each shrid
    for shrid_id in gdf["shrid2"].unique():
        selected_data = gdf[gdf["shrid2"] == shrid_id]
        if selected_data.empty:
            continue

        selected_polygon = selected_data["geometry"].iloc[0]
        heatmap_data = [
            [row[lat_col], row[lon_col], row['PCA_1']]
            for _, row in selected_data.iterrows()
            if selected_polygon.contains(Point(row[lon_col], row[lat_col]))
        ]

        # If no data points fall inside the polygon, skip
        if not heatmap_data:
            continue

        x_min, y_min, x_max, y_max = selected_polygon.bounds
        map_center = [(y_min + y_max) / 2, (x_min + x_max) / 2]

        m = folium.Map(location=map_center, zoom_start=zoom_start)
        folium.Polygon(
            locations=[(p[1], p[0]) for p in selected_polygon.exterior.coords],
            color='blue', weight=2, fill=True, fill_opacity=0.2
        ).add_to(m)
        HeatMap(heatmap_data).add_to(m)

        html_file = os.path.join(output_folder, f"polygon_with_heatmap_{shrid_id}.html")
        m.save(html_file)