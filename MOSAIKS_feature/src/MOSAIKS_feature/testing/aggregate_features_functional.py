import pandas as pd

class aggregateFeatures:
    def __init__(self, file_path, output_file):
        self.file_path = file_path
        self.output_file = output_file
        self.df = None
        self.feature_columns = []
        self.average_features_df = None

    def load_data(self):
        """Load the dataset."""
        self.df = pd.read_csv(self.file_path)

    def fill_missing_values(self):
        """Fill NaN values with 0."""
        if self.df is not None:
            self.df = self.df.fillna(0)

    def identify_feature_columns(self):
        """Identify feature columns (all columns except 'shrid2', 'Lat', and 'Lon')."""
        if self.df is not None:
            self.feature_columns = [col for col in self.df.columns if col not in ['shrid2', 'Lat', 'Lon']]

    def calculate_averages(self):
        """Group by 'shrid2' and calculate the mean for each feature column."""
        if self.df is not None and self.feature_columns:
            self.average_features_df = self.df.groupby('shrid2')[self.feature_columns].mean().reset_index()

    def save_results(self):
        """Save the averaged features to a file."""
        if self.average_features_df is not None:
            self.average_features_df.to_csv(self.output_file, index=False)
            print(f"Averaged features saved to {self.output_file}")

    def process(self):
        """Run the full process."""
        self.load_data()
        self.fill_missing_values()
        self.identify_feature_columns()
        self.calculate_averages()
        self.save_results()