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
        coord_string = "[(12.5012, -45.1234), (13.5432, -44.9876), (12.9987, -45.0021), (13.2345, -45.5001), (12.5012, -45.1234)]"
        polygon = createPolygon(coord_string)
        
        self.assertIsInstance(polygon, Polygon)
        self.assertEqual(len(polygon.exterior.coords), 5)
        self.assertEqual(polygon.exterior.coords[0], (12.5012, -45.1234))
    
    def test_point_in_polygon(self):
        coord_string = "[(30.2314, 10.1234), (30.2330, 10.1235), (30.2340, 10.1225), (30.2335, 10.1210), (30.2314, 10.1234)]"
        polygon = createPolygon(coord_string)
        
        min_lon, max_lon = 30.20, 30.25
        min_lat, max_lat = 10.10, 10.13
        num_points_x = np.arange(min_lon, max_lon + 0.005, 0.005)
        num_points_y = np.arange(min_lat, max_lat + 0.005, 0.005)
        x_grid, y_grid = np.meshgrid(num_points_x, num_points_y)

        lons = x_grid.flatten()
        lats = y_grid.flatten()
        valid_points = []

        for coord in zip(lons, lats):
            point = Point(float(coord[0]), float(coord[1]))
            if polygon.contains(point):
                valid_points.append(point)
        
        self.assertEqual(len(valid_points), 0, "Unexpected points found within the polygon.")
    
    def test_grid_generation_limits(self):
        min_lon, max_lon = 50.55, 51.75
        min_lat, max_lat = -22.45, -21.85
        num_points_x = int((max_lon - min_lon) / 0.01) + 1
        num_points_y = int((max_lat - min_lat) / 0.01) + 1
        x_range = np.linspace(min_lon, max_lon, num_points_x)
        y_range = np.linspace(min_lat, max_lat, num_points_y)
        
        self.assertAlmostEqual(x_range[0], min_lon)
        self.assertAlmostEqual(x_range[-1], max_lon)
        self.assertAlmostEqual(y_range[0], min_lat)
        self.assertAlmostEqual(y_range[-1], max_lat)

class TestPolygonEdgeCases(unittest.TestCase):

    def test_minimum_vertices_polygon(self):
        coord_string = "[(88.1234, 25.4567), (88.2345, 25.5678), (88.3456, 25.6789), (88.1234, 25.4567)]"
        polygon = createPolygon(coord_string)
        self.assertIsInstance(polygon, Polygon)
        self.assertEqual(len(polygon.exterior.coords), 4)

    def test_invalid_input_format(self):
        with self.assertRaises(SyntaxError):
            createPolygon("Invalid input")

    def test_collinear_points(self):
        coord_string = "[(55.9876, 12.3456), (56.1234, 12.3456), (56.2345, 12.3456), (55.9876, 12.3456)]"
        polygon = createPolygon(coord_string)
        self.assertEqual(polygon.area, 0, "Polygon should have zero area with collinear points")

    def test_negative_coordinates(self):
        coord_string = "[(-130.1234, -60.2345), (-130.1234, -60.4345), (-130.3234, -60.4345), (-130.3234, -60.2345), (-130.1234, -60.2345)]"
        polygon = createPolygon(coord_string)
        self.assertIsInstance(polygon, Polygon)
        
        # Point just outside the bounds
        point_outside = Point(-130.5, -60.5)
        # Point closer to the center of the polygon
        point_inside = Point(-130.2, -60.3)
        
        # Assertions
        self.assertFalse(polygon.contains(point_outside))
        self.assertTrue(polygon.contains(point_inside))

    def test_large_polygon_shape(self):
        coord_string = str([(float(np.cos(theta) * 120.5678), float(np.sin(theta) * -45.6789)) for theta in np.linspace(0, 2 * np.pi, 51)])
        polygon = createPolygon(coord_string)
        self.assertIsInstance(polygon, Polygon)
        self.assertEqual(len(polygon.exterior.coords), 52)

    def test_point_outside_polygon(self):
        coord_string = "[(140.2345, -33.1234), (140.3456, -33.2345), (140.4567, -33.3456), (140.2345, -33.4567), (140.2345, -33.1234)]"
        polygon = createPolygon(coord_string)
        outside_point = Point(141.0, -33.0)
        self.assertFalse(polygon.contains(outside_point))

    def test_boundary_point_check(self):
        """Boundary point should be excluded if only using polygon.contains"""
        coord_string = "[(78.1234, 14.5678), (78.2345, 14.6789), (78.3456, 14.7890), (78.1234, 14.5678)]"
        polygon = createPolygon(coord_string)
        boundary_point = Point(78.1234, 14.5678)
        self.assertFalse(polygon.contains(boundary_point),
                         "Boundary point should not be considered inside the polygon when using contains")

if __name__ == "__main__":
    unittest.main()