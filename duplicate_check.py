import pandas as pd

# Load the CSV file
data = pd.read_csv('/Users/sammizhu/SUPER/strategy2/matches_shrid2.csv')

# Check for duplicate rows based on 'Lat' and 'Lon'
duplicates = data.duplicated(subset=['Lat', 'Lon'], keep=False)

# Count how many duplicates there are
num_duplicates = duplicates.sum()

# Print the number of duplicate rows
print(f'Total number of duplicate rows based on Lat and Lon: {num_duplicates}')