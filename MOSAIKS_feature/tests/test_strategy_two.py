import unittest
import pandas as pd
import os
from shapely.geometry import Polygon
from io import StringIO
from src.MOSAIKS_feature.strategy_two import compute_bounding_box, process_shrid_bounding_boxes, parse_polygon, visualize_boundary_boxes

class TestBoundingBoxFunctions(unittest.TestCase):
    def setUp(self):
        # Sample polygon CSV content for testing
        self.sample_csv = StringIO("""
shrid2,polygon_coordinates
1,"[(0,0), (0,2), (2,2), (2,0)]"
2,"[(1,1), (1,3), (3,3), (3,1)]"
""")
        self.sample_df = pd.read_csv(self.sample_csv)

    def test_compute_bounding_box(self):
        # Test bounding box calculation for a square polygon
        polygon = Polygon([(0, 0), (0, 2), (2, 2), (2, 0)])
        min_lat, max_lat, min_lon, max_lon = compute_bounding_box(polygon)
        self.assertEqual((min_lat, max_lat, min_lon, max_lon), (0, 2, 0, 2))
    
    def test_process_shrid_bounding_boxes(self):
        # Save test CSV for function input
        test_file = "test_polygons.csv"
        self.sample_df.to_csv(test_file, index=False)
        
        # Run function and check output
        output_file = process_shrid_bounding_boxes(test_file)
        self.assertTrue(os.path.exists(output_file), "Output file was not created.")
        
        # Load output file and check contents
        output_df = pd.read_csv(output_file)
        self.assertIn("min_lat", output_df.columns)
        self.assertIn("centroid_x", output_df.columns)
        self.assertEqual(len(output_df), 2)
        
        os.remove(test_file)
        os.remove(output_file)
    
    def test_parse_polygon(self):
        # Test the conversion of string to shapely polygon
        polygon_string = "[(0,0), (0,2), (2,2), (2,0)]"
        polygon = parse_polygon(polygon_string)
        self.assertIsInstance(polygon, Polygon, "Parsed result is not a Polygon.")
        self.assertTrue(polygon.is_valid, "Polygon is not valid.")
    
    def test_visualize_boundary_boxes(self):
        # Generate test CSV with at least 10 rows
        polygons = [
            "[(0,0), (0,2), (2,2), (2,0)]",
            "[(1,1), (1,3), (3,3), (3,1)]",
            "[(2,2), (2,4), (4,4), (4,2)]",
            "[(3,3), (3,5), (5,5), (5,3)]",
            "[(4,4), (4,6), (6,6), (6,4)]",
            "[(5,5), (5,7), (7,7), (7,5)]",
            "[(6,6), (6,8), (8,8), (8,6)]",
            "[(7,7), (7,9), (9,9), (9,7)]",
            "[(8,8), (8,10), (10,10), (10,8)]",
            "[(9,9), (9,11), (11,11), (11,9)]"
        ]
        test_data = pd.DataFrame({
            'shrid2': range(1, 11),
            'polygon_coordinates': polygons
        })
        
        # Save the test data to a CSV
        test_file = "test_visualize.csv"
        test_data.to_csv(test_file, index=False)
        
        # Run process_shrid_bounding_boxes to compute bounding box columns
        output_file = process_shrid_bounding_boxes(test_file)

        try:
            # Run visualization on the processed file
            visualize_boundary_boxes(output_file)
        except Exception as e:
            self.fail(f"visualize_boundary_boxes raised an error: {e}")
        finally:
            # Cleanup test files
            os.remove(test_file)
            os.remove(output_file)

if __name__ == '__main__':
    unittest.main()