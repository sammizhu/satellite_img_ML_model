import pandas as pd

# Load the CSV files
map_df = pd.read_csv('/Users/sammizhu/SUPER/3.csv')
file_df = pd.read_csv('/Users/sammizhu/SUPER/file_coordinates.csv')

# Assuming the columns for latitude and longitude are named 'lat' and 'long'
# Adjust column names based on your CSV structure
map_coords = set(zip(map_df['Lat'], map_df['Lon']))
file_coords = set(zip(file_df['Lat'], file_df['Lon']))

# Find the intersection (shared latitude and longitude pairs)
shared_coords = map_coords.intersection(file_coords)

# Count the number of shared pairs
num_shared = len(shared_coords)

print(f"Number of shared lat, long pairs: {num_shared}")

# Find the coordinates that are in map.csv but not in file.csv
map_only_coords = map_coords - file_coords

# Print the coordinates
print(f"Coordinates in map.csv but not in file.csv: {map_only_coords}")

# Find the coordinates that are in file.csv but not in map.csv
file_only_coords = file_coords - map_coords 

# Print the coordinates
print(f"Coordinates in file.csv but not in map.csv: {file_only_coords}")
