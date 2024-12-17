import unittest
from unittest.mock import patch
import pandas as pd
from io import StringIO
from src.MOSAIKS_feature.misc import DuplicateCheck, Merge, Subset, Unique 


class TestCSVOperations(unittest.TestCase):

    def setUp(self):
        # Mock CSV data
        self.test_data = pd.read_csv(StringIO(
            "Lat,Lon,Value\n"
            "34.05,-118.25,100\n"
            "34.05,-118.25,200\n"
            "40.71,-74.00,300\n"
            "37.77,-122.41,400\n"
        ))
        self.test_data_b = pd.read_csv(StringIO(
            "Lat,Lon,Description\n"
            "34.05,-118.25,Los Angeles\n"
            "40.71,-74.00,New York\n"
            "37.77,-122.41,San Francisco\n"
        ))

    @patch("pandas.read_csv")
    def test_duplicate_check(self, mock_read_csv):
        # Mock pandas.read_csv to return test_data
        mock_read_csv.return_value = self.test_data
        # Call the DuplicateCheck function
        num_duplicates = DuplicateCheck.check_duplicates("mock_path.csv", ["Lat", "Lon"])
        self.assertEqual(num_duplicates, 2, "Number of duplicates should be 2")

    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_merge(self, mock_to_csv, mock_read_csv):
        # Mock pandas.read_csv for both input files
        mock_read_csv.side_effect = [self.test_data, self.test_data_b]
        # Call the Merge function
        Merge.merge_files("mock_file_a.csv", "mock_file_b.csv", ["Lat", "Lon"], "mock_output.csv")
        # Ensure to_csv is called once
        mock_to_csv.assert_called_once()

    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_csv")
    def test_subset(self, mock_to_csv, mock_read_csv):
        # Mock pandas.read_csv
        mock_read_csv.return_value = self.test_data
        # Call the Subset function
        Subset.fetch_and_save_first_n_rows("mock_input.csv", "mock_output.csv", 2)
        # Ensure to_csv is called once
        mock_to_csv.assert_called_once()

    @patch("pandas.read_csv")
    def test_unique(self, mock_read_csv):
        # Mock pandas.read_csv
        mock_read_csv.return_value = self.test_data
        # Call the Unique function
        num_distinct = Unique.count_distinct_rows("mock_path.csv", ["Lat", "Lon"])
        self.assertEqual(num_distinct, 3, "Number of distinct rows should be 3")


if __name__ == "__main__":
    unittest.main()