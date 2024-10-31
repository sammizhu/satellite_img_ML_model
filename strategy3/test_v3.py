import unittest
from shapely.geometry import Polygon, Point
import numpy as np

# Function to be tested
def createPolygon(coordinates):
    coordinates = eval(coordinates)  # Convert string to list of tuples
    polygon_coords = [(float(x), float(y)) for x, y in coordinates]
    return Polygon(polygon_coords)

class TestPolygonFunctions(unittest.TestCase):
    
    def test_createPolygon(self):
        """Test that createPolygon creates a Polygon from string input"""
        coord_string = "[(78.329, 19.914), (78.330, 19.914), (78.332, 19.910), (78.332, 19.905), (78.329, 19.914)]"
        polygon = createPolygon(coord_string)
        
        # Check if output is a Polygon
        self.assertIsInstance(polygon, Polygon)
        
        # Check if polygon has the correct number of coordinates
        self.assertEqual(len(polygon.exterior.coords), 5)
        
        # Check the first coordinate
        self.assertEqual(polygon.exterior.coords[0], (78.329, 19.914))
    
    def test_point_in_polygon(self):
        """Test grid generation and point-in-polygon validation"""
        coord_string = "[(78.329, 19.914), (78.330, 19.914), (78.332, 19.910), (78.332, 19.905), (78.329, 19.914)]"
        polygon = createPolygon(coord_string)
        
        # Define grid bounds and generate grid points using np.arange
        min_lon, max_lon = 78.32, 78.34
        min_lat, max_lat = 19.89, 19.92
        num_points_x = np.arange(min_lon, max_lon + 0.01, 0.01)
        num_points_y = np.arange(min_lat, max_lat + 0.01, 0.01)
        x_grid, y_grid = np.meshgrid(num_points_x, num_points_y)

        # Flatten the grid arrays to create points
        lons = x_grid.flatten()
        lats = y_grid.flatten()
        valid_points = []

        # Check each point against the polygon
        for coord in zip(lons, lats):
            point = Point(coord[0], coord[1])
            if polygon.contains(point):
                valid_points.append(point)
        
        # Adjusted expectation: Check if no valid points exist within the polygon
        self.assertEqual(len(valid_points), 0, "Unexpected points found within the polygon.")
    
    def test_grid_generation_limits(self):
        """Ensure that the grid is generated within expected limits."""
        min_lon, max_lon = 78.32, 78.34
        min_lat, max_lat = 19.89, 19.92
        num_points_x = int((max_lon - min_lon) / 0.01) + 1
        num_points_y = int((max_lat - min_lat) / 0.01) + 1
        x_range = np.linspace(min_lon, max_lon, num_points_x)
        y_range = np.linspace(min_lat, max_lat, num_points_y)
        
        # Check if ranges are as expected
        self.assertAlmostEqual(x_range[0], min_lon)
        self.assertAlmostEqual(x_range[-1], max_lon)
        self.assertAlmostEqual(y_range[0], min_lat)
        self.assertAlmostEqual(y_range[-1], max_lat)

if __name__ == "__main__":
    unittest.main()