import unittest
import os
import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point
from MOSAIKS_feature.granular_coords import PolygonGridGenerator

class TestPolygonGridGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Create a temporary mock CSV file for testing."""
        cls.mock_csv_file = "mock_test_file.csv"
        mock_data = {
            "min_lat": [10.0, 20.0],
            "max_lat": [10.2, 20.2],
            "min_lon": [30.0, 40.0],
            "max_lon": [30.2, 40.2],
            "shrid2": [1, 2],
            "Unnamed: 0": [1, 2],
            "polygon_coordinates": [
                "[(30.0, 10.0), (30.2, 10.0), (30.2, 10.2), (30.0, 10.2), (30.0, 10.0)]",
                "[(40.0, 20.0), (40.2, 20.0), (40.2, 20.2), (40.0, 20.2), (40.0, 20.0)]",
            ],
        }
        pd.DataFrame(mock_data).to_csv(cls.mock_csv_file, index=False)

    @classmethod
    def tearDownClass(cls):
        """Remove the temporary mock CSV file."""
        if os.path.exists(cls.mock_csv_file):
            os.remove(cls.mock_csv_file)

    def test_create_polygon(self):
        generator = PolygonGridGenerator(self.mock_csv_file)
        coord_string = "[(12.5012, -45.1234), (13.5432, -44.9876), (12.9987, -45.0021), (13.2345, -45.5001), (12.5012, -45.1234)]"
        polygon = generator.create_polygon(coord_string)

        self.assertIsInstance(polygon, Polygon)
        self.assertEqual(len(polygon.exterior.coords), 5)
        self.assertEqual(polygon.exterior.coords[0], (12.5012, -45.1234))

    def test_preprocess_coordinates(self):
        generator = PolygonGridGenerator(self.mock_csv_file)
        generator.preprocess_coordinates()

        self.assertAlmostEqual(generator.data["min_lat_round"].iloc[0], 10.005)
        self.assertAlmostEqual(generator.data["max_lat_round"].iloc[0], 10.195)
        self.assertAlmostEqual(generator.data["min_lon_round"].iloc[0], 30.005)
        self.assertAlmostEqual(generator.data["max_lon_round"].iloc[0], 30.195)

    def test_generate_grid(self):
        generator = PolygonGridGenerator(self.mock_csv_file)
        generator.preprocess_coordinates()
        generator.generate_grid()

        self.assertIsNotNone(generator.result_df)
        self.assertGreater(generator.result_df.shape[0], 0, "Grid generation failed to create valid points")

    def test_save_to_csv(self):
        generator = PolygonGridGenerator(self.mock_csv_file)
        generator.preprocess_coordinates()
        generator.generate_grid()

        # Save generated data to CSV files
        generator.save_to_csv(chunk_size=2)

        # Verify the files were created
        for i in range(1, 2 + 1):  # 2 rows in total, chunk size = 2
            file_name = f"file_coordinates_{i}.csv"
            self.assertTrue(os.path.exists(file_name))
            os.remove(file_name)  # Clean up after the test

    def test_point_in_polygon(self):
        generator = PolygonGridGenerator(self.mock_csv_file)
        coord_string = "[(30.2314, 10.1234), (30.2330, 10.1235), (30.2340, 10.1225), (30.2335, 10.1210), (30.2314, 10.1234)]"
        polygon = generator.create_polygon(coord_string)

        min_lon, max_lon = 30.20, 30.25
        min_lat, max_lat = 10.10, 10.13
        x_grid, y_grid = np.meshgrid(np.arange(min_lon, max_lon + 0.005, 0.005),
                                     np.arange(min_lat, max_lat + 0.005, 0.005))

        valid_points = [
            (lon, lat) for lon, lat in zip(x_grid.flatten(), y_grid.flatten())
            if polygon.contains(Point(lon, lat))
        ]

        self.assertEqual(len(valid_points), 0, "Unexpected points found within the polygon")
    
    def generate_grid_no_polygon(self):
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
        self.lons_list = np.hstack(lons_list) if lons_list else np.array([])
        self.lats_list = np.hstack(lats_list) if lats_list else np.array([])
        self.shrid_id_list = np.hstack(shrid_id_list) if shrid_id_list else np.array([])
        self.id_count_list = np.hstack(id_count_list) if id_count_list else np.array([])


if __name__ == "__main__":
    unittest.main()