import pandas as pd

def fetch_and_save_first_100_rows(input_csv_file_path, output_csv_file_path):
    # Read the first 100 rows from the input CSV file
    df = pd.read_csv(input_csv_file_path, nrows=5000)
    
    # Save the DataFrame to a new CSV file
    df.to_csv(output_csv_file_path, index=False)

# Example usage
input_csv_file_path = '/Users/sammizhu/SUPER/[RAW]_Strategy_3_Features.csv'
output_csv_file_path = '/Users/sammizhu/SUPER/subset_raw_features.csv'
fetch_and_save_first_100_rows(input_csv_file_path, output_csv_file_path)

print(f"First 100 rows saved to {output_csv_file_path}")