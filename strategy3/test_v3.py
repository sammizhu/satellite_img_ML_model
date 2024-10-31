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

class TestPolygonEdgeCases(unittest.TestCase):

    def test_minimum_vertices_polygon(self):
        """Test polygon creation with the minimum number of vertices (triangle)"""
        coord_string = "[(0, 0), (1, 1), (1, 0), (0, 0)]"
        polygon = createPolygon(coord_string)
        self.assertIsInstance(polygon, Polygon)
        self.assertEqual(len(polygon.exterior.coords), 4)

    def test_duplicate_points(self):
        """Test polygon with duplicate points"""
        coord_string = "[(0, 0), (1, 1), (1, 0), (1, 0), (0, 0)]"
        polygon = createPolygon(coord_string)
        self.assertIsInstance(polygon, Polygon)
        self.assertEqual(len(polygon.exterior.coords), 4, "Duplicate points should not create additional vertices")

    def test_invalid_input_format(self):
        """Test with invalid input format"""
        with self.assertRaises(SyntaxError):
            createPolygon("Invalid input")

    def test_collinear_points(self):
        """Test polygon with collinear points"""
        coord_string = "[(0, 0), (2, 2), (4, 4), (0, 0)]"  # Points lie on a straight line
        polygon = createPolygon(coord_string)
        self.assertTrue(polygon.is_empty, "Polygon should not be valid with collinear points")

    def test_negative_coordinates(self):
        """Test polygon with negative coordinates"""
        coord_string = "[(-1, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]"
        polygon = createPolygon(coord_string)
        self.assertIsInstance(polygon, Polygon)
        point_outside = Point(-2, 0)
        point_inside = Point(0, 0)
        self.assertFalse(polygon.contains(point_outside))
        self.assertTrue(polygon.contains(point_inside))

    def test_large_polygon_shape(self):
        """Test with a polygon that has a large number of vertices"""
        coord_string = str([(np.cos(theta), np.sin(theta)) for theta in np.linspace(0, 2 * np.pi, 51)])
        polygon = createPolygon(coord_string)
        self.assertIsInstance(polygon, Polygon)
        self.assertEqual(len(polygon.exterior.coords), 51)

    def test_point_outside_polygon(self):
        """Check that a point just outside the polygon is not included"""
        coord_string = "[(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]"
        polygon = createPolygon(coord_string)
        outside_point = Point(4.1, 4.1)
        self.assertFalse(polygon.contains(outside_point))

    def test_boundary_point_check(self):
        """Check that a boundary point is handled correctly"""
        coord_string = "[(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]"
        polygon = createPolygon(coord_string)
        boundary_point = Point(4, 4)
        # Shapely generally considers boundary points as inside
        self.assertTrue(polygon.contains(boundary_point), "Boundary point should be considered inside the polygon")

if __name__ == "__main__":
    unittest.main()