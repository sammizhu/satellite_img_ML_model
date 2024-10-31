import pandas as pd

# Load the dataset
file_path = 'your_input_file.csv'  # Replace with your file path
df = pd.read_csv(file_path)

# Step 1: Group by 'shrid2' and 'feature_name' and calculate the mean of 'feature_value'
average_features = df.groupby(['shrid2', 'feature_name'])['feature_value'].mean().reset_index()

# Step 2: Pivot the table to have each feature as a separate column
average_features_pivot = average_features.pivot(index='shrid2', columns='feature_name', values='feature_value').reset_index()

# Step 3: Output to a new file
output_file = 'averaged_features_by_shrid2.csv'
average_features_pivot.to_csv(output_file, index=False)

print(f"Averaged features saved to {output_file}")