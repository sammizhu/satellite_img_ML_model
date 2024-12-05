import pandas as pd

# Load the dataset and rename duplicate columns
file_path = ''
df = pd.read_csv(file_path)

# Fill NaN values with 0 for averaging
df = df.fillna(0)

# Identify feature columns (all columns except 'shrid2', 'Lat', and 'Lon')
feature_columns = [col for col in df.columns if col not in ['shrid2', 'Lat', 'Lon']]

# Group by 'shrid2' and calculate the mean for each feature column
average_features_df = df.groupby('shrid2')[feature_columns].mean().reset_index()

# Save the result to a new file (without Lat and Lon)
output_file = ''
average_features_df.to_csv(output_file, index=False)

print(f"Averaged features saved to {output_file}")