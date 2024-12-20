import unittest
import pandas as pd
import os
from io import StringIO
from src.MOSAIKS_feature.testing.aggregate_features_functional import aggregateFeatures 

class TestFeatureAverager(unittest.TestCase):

    def setUp(self):
        # Create a sample dataset for testing
        self.data = StringIO(
            """shrid2,Lat,Lon,feature1,feature2,feature3
            1,10.0,20.0,5.0,,15.0
            1,10.0,20.0,15.0,25.0,
            2,30.0,40.0,,5.0,25.0
            2,30.0,40.0,10.0,,35.0"""
        )
        self.file_path = "test_input.csv"
        self.output_file = "test_output.csv"
        pd.read_csv(self.data).to_csv(self.file_path, index=False)

        self.averager = aggregateFeatures(self.file_path, self.output_file)

    def test_fill_missing_values(self):
        self.averager.load_data()
        self.averager.fill_missing_values()
        self.assertTrue((self.averager.df.isna().sum().sum() == 0))

    def test_identify_feature_columns(self):
        self.averager.load_data()
        self.averager.identify_feature_columns()
        self.assertListEqual(self.averager.feature_columns, ['feature1', 'feature2', 'feature3'])

    def test_calculate_averages(self):
        self.averager.load_data()
        self.averager.fill_missing_values()
        self.averager.identify_feature_columns()
        self.averager.calculate_averages()

        expected_data = {
            'shrid2': [1, 2],
            'feature1': [10.0, 5.0],
            'feature2': [12.5, 2.5],
            'feature3': [7.5, 30.0],
        }
        expected_df = pd.DataFrame(expected_data)

        pd.testing.assert_frame_equal(self.averager.average_features_df, expected_df)

    def test_save_results(self):
        self.averager.load_data()
        self.averager.fill_missing_values()
        self.averager.identify_feature_columns()
        self.averager.calculate_averages()
        self.averager.save_results()

        # Check if the file is created
        self.assertTrue(os.path.exists(self.output_file))

        # Verify the contents of the file
        saved_df = pd.read_csv(self.output_file)
        expected_data = {
            'shrid2': [1, 2],
            'feature1': [10.0, 5.0],
            'feature2': [12.5, 2.5],
            'feature3': [7.5, 30.0],
        }
        expected_df = pd.DataFrame(expected_data)
        pd.testing.assert_frame_equal(saved_df, expected_df)

    def tearDown(self):
        # Clean up any created files
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

if __name__ == "__main__":
    unittest.main()