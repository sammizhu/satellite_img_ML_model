import pandas as pd

# Load the CSV file
data = pd.read_csv('/Users/sammizhu/SUPER/strategy2/strategy2_features.csv')

# Drop duplicate rows based on 'Lat' and 'Lon' to get distinct rows
distinct_rows = data.drop_duplicates(subset=['Lat', 'Lon'])

# Count the number of distinct rows
num_distinct = len(distinct_rows)

# Print the number of distinct rows
print(f'Total number of distinct rows based on Lat and Lon: {num_distinct}')