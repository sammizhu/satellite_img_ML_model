import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import GoogleV3
from geopy.distance import geodesic
import warnings
warnings.filterwarnings("ignore")
from geopy.exc import GeocoderTimedOut
from PIL import Image
from io import BytesIO
import geopandas as gpd
import matplotlib.patches as patches
from shapely.geometry import Polygon, Point, box


def compute_bounding_box(polygon):
    minx, miny, maxx, maxy = polygon.bounds
    return miny, maxy, minx, maxx  # Returning (min lat, max lat, min lon, max lon)
    
    
def process_shrid_bounding_boxes(csv_file):
    # Load the CSV file
    df = pd.read_csv(csv_file)
    
    # Initialize lists to store bounding box results
    min_lats = []
    max_lats = []
    min_lons = []
    max_lons = []
    centroids = []
    
    
    for index, row in df.iterrows():
        polygon = Polygon(eval(row['polygon_coordinates']))
        
        # Compute the bounding box
        min_lat, max_lat, min_lon, max_lon = compute_bounding_box(polygon)
        
        # Store the results
        min_lats.append(min_lat)
        max_lats.append(max_lat)
        min_lons.append(min_lon)
        max_lons.append(max_lon)
         
        # Calculate and Save centroid data
        centroids.append((polygon.centroid.x, polygon.centroid.y)) 
   

    
    # Add results to the dataframe
    df['min_lat'] = min_lats
    df['max_lat'] = max_lats
    df['min_lon'] = min_lons
    df['max_lon'] = max_lons
    df['centroid_x'] = [centroid[0] for centroid in centroids]
    df['centroid_y'] = [centroid[1] for centroid in centroids]

    
    # Save results to a new CSV file
    output_file = "shrid_bounding_boxes_for_mosaiks.csv"
    df.to_csv(output_file, index=False)
    
    return output_file


## Visualizing Boundary Boxes
def vis_boundary_boxes(csv_file_path):

    shrid_data = pd.read_csv(csv_file_path)

    # Function to convert polygon coordinates to a shapely Polygon object
    def parse_polygon(polygon_string):
        coordinates = eval(polygon_string)
        return Polygon(coordinates)

    # Convert polygon coordinates into shapely objects
    shrid_data['geometry'] = shrid_data['polygon_coordinates'].apply(parse_polygon)

    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(shrid_data, geometry='geometry')

    # Function to create a bounding box Polygon from min/max lat/lon
    def create_bbox(minx, miny, maxx, maxy):
        return box(minx, miny, maxx, maxy)

    # Apply the function to create bounding boxes
    gdf['bbox'] = gdf.apply(lambda row: create_bbox(row['min_lon'], row['min_lat'], row['max_lon'], row['max_lat']), axis=1)

    # Select any 10 shrid polygons for visualization
    gdf_sample = gdf.sample(10)

    # Plot each polygon with its bounding box and centroid separately
    for index, row in gdf_sample.iterrows():
        fig, ax = plt.subplots(figsize=(10, 10))  # Adjust the figure size as needed

        # Plot the polygon
        gdf_single = gpd.GeoDataFrame([row], geometry='geometry')
        gdf_single.plot(ax=ax, edgecolor='blue', facecolor='orange', linewidth=3)

        # Plot the bounding box
        gdf_bbox = gpd.GeoDataFrame([row], geometry='bbox')
        gdf_bbox.plot(ax=ax, edgecolor='green', facecolor='none', linewidth=2, linestyle='--')

        # Plot the centroid (provided in the CSV file)
        ax.plot(row['centroid_x'], row['centroid_y'], 'ro', markersize=10, label='Centroid')

        # Customize plot appearance
        plt.title(f'shrid: {row["shrid2"]}', fontsize=16)
        plt.xlabel('Longitude', fontsize=12)
        plt.ylabel('Latitude', fontsize=12)
        ax.set_aspect('equal')  # Keep the aspect ratio of the plot equal
        ax.legend()

        # Show the plot
        plt.show()