import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point

class PolygonGridGenerator:
    def __init__(self, csv_file):
        """Initialize the class with a CSV file."""
        self.csv_file = csv_file
        self.data = pd.read_csv(csv_file)
        self.result_df = None

    @staticmethod
    def create_polygon(coordinates):
        """Convert a string representation of coordinates to a Shapely Polygon."""
        coordinates = eval(coordinates)
        polygon_coords = [(float(x), float(y)) for x, y in coordinates]
        return Polygon(polygon_coords)

    def preprocess_coordinates(self):
        """Round and adjust the coordinates in the DataFrame."""
        self.data["min_lat_round"] = self.data["min_lat"].round(2) + 0.005
        self.data["max_lat_round"] = self.data["max_lat"].round(2) - 0.005
        self.data["min_lon_round"] = self.data["min_lon"].round(2) + 0.005
        self.data["max_lon_round"] = self.data["max_lon"].round(2) - 0.005

    def generate_grid(self):
        """Generate a grid of valid coordinates for each polygon."""
        lons_list = []
        lats_list = []
        shrid_id_list = []
        id_count_list = []

        for i, row in self.data.iterrows():
            polygon = self.create_polygon(row["polygon_coordinates"])

            # Generate coordinate ranges
            x_range = np.arange(row["min_lon_round"], row["max_lon_round"] + 0.01, 0.01)
            y_range = np.arange(row["min_lat_round"], row["max_lat_round"] + 0.01, 0.01)
            x_grid, y_grid = np.meshgrid(x_range, y_range)

            lons = x_grid.flatten()
            lats = y_grid.flatten()

            # Validate coordinates using the point-in-polygon test
            valid_lons = []
            valid_lats = []
            for lon, lat in zip(lons, lats):
                point = Point(lon, lat)
                if polygon.contains(point):
                    valid_lons.append(lon)
                    valid_lats.append(lat)

            # Append valid results to the lists
            if valid_lons and valid_lats:
                shrid_id = np.full(len(valid_lons), row["shrid2"])
                id_count = np.full(len(valid_lons), row["Unnamed: 0"])

                lons_list.append(valid_lons)
                lats_list.append(valid_lats)
                shrid_id_list.append(shrid_id)
                id_count_list.append(id_count)

        # Combine results into flat arrays
        self.result_df = pd.DataFrame({
            "Unnamed: 0": np.hstack(id_count_list),
            "file2": np.hstack(shrid_id_list),
            "Lon": np.hstack(lons_list),
            "Lat": np.hstack(lats_list)
        })

    def generate_grid_no_polygon(self):
        """Generate coordinate grids without comparing with polygon coordinate"""
        # Round and adjust the coordinates
        self.csv_file["min_lat_round"] = self.csv_file["min_lat"].round(2) + .005
        self.csv_file["max_lat_round"] = self.csv_file["max_lat"].round(2) - .005
        self.csv_file["min_lon_round"] = self.csv_file["min_lon"].round(2) + .005
        self.csv_file["max_lon_round"] = self.csv_file["max_lon"].round(2) - .005

        # Initialize lists to store the results
        lons_list = []
        lats_list = []
        shrid_id_list = []
        id_count_list = []

        # Iterate over each row in the DataFrame to generate a grid of coordinates
        for i, row in self.csv_file.iterrows():
            x_range = np.arange(row["min_lon_round"], row["max_lon_round"] + 0.01, 0.01)
            y_range = np.arange(row["min_lat_round"], row["max_lat_round"] + 0.01, 0.01)
            x_grid, y_grid = np.meshgrid(x_range, y_range)

            lons = x_grid.flatten()
            lats = y_grid.flatten()

            # Filter both lons and lats based on the current row's min/max bounds
            # Ensures no out-of-bound region errors 
            valid_indices = (lons >= row["min_lon"]) & (lons <= row["max_lon"]) & \
                            (lats >= row["min_lat"]) & (lats <= row["max_lat"])
            
            lons_filtered = lons[valid_indices]
            lats_filtered = lats[valid_indices]

            # If filtered arrays are not empty, append the corresponding shrid2 values
            if len(lons_filtered) > 0 and len(lats_filtered) > 0:
                shrid_id = np.full(len(lons_filtered), row["shrid2"])
                id_count = np.full(len(lons_filtered), row["Unnamed: 0"])

                lons_list.append(lons_filtered)
                lats_list.append(lats_filtered)
                shrid_id_list.append(shrid_id)
                id_count_list.append(id_count)

        # Combine all the individual lists into single flat arrays
        lons_list = np.hstack(lons_list)
        lats_list = np.hstack(lats_list)
        shrid_id_list = np.hstack(shrid_id_list)
        id_count_list = np.hstack(id_count_list)

    def save_to_csv(self, chunk_size=100000):
        """Save the resulting DataFrame to one or more CSV files."""
        total_rows = self.result_df.shape[0]
        num_chunks = (total_rows // chunk_size) + 1

        for i in range(num_chunks):
            start_row = i * chunk_size
            end_row = min((i + 1) * chunk_size, total_rows)

            chunk_df = self.result_df.iloc[start_row:end_row]
            chunk_filename = f"file_coordinates_{i + 1}.csv"
            chunk_df.to_csv(chunk_filename, index=False, float_format="%.3f")

            print(f"Saved {chunk_filename} with rows {start_row} to {end_row - 1}")

    def run(self):
        """Execute the full pipeline."""
        self.preprocess_coordinates()
        self.generate_grid()
        self.save_to_csv()