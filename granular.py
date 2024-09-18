import pandas as pd
import numpy as np

# Read the CSV file into a DataFrame
shrid = pd.read_csv("/Users/sammizhu/SUPER/test.csv")

# Round and adjust the coordinates
shrid["min_lat_round"] = (shrid["min_lat"] + .01).round(2) + .005
shrid["max_lat_round"] = (shrid["max_lat"] + .01).round(2) - .005
shrid["min_lon_round"] = (shrid["min_lon"] + .01).round(2) + .005
shrid["max_lon_round"] = (shrid["max_lon"] + .01).round(2) - .005

# Initialize lists to store the results
lons_list = []
lats_list = []
shrid_id_list = []

# Iterate over each row in the DataFrame to generate a grid of coordinates
for i, row in shrid.iterrows():
    x_range = np.arange(row["min_lon_round"], row["max_lon_round"] + .01, .01)
    y_range = np.arange(row["min_lat_round"], row["max_lat_round"] + .01, .01)
    x_grid, y_grid = np.meshgrid(x_range, y_range)

    lons = x_grid.flatten()
    lats = y_grid.flatten()
    shrid_id = np.full(len(lons), row["shrid2"])

    lons_list.append(lons)
    lats_list.append(lats)
    shrid_id_list.append(shrid_id)

# Combine all the individual lists into single flat arrays
lons_list = np.hstack(lons_list)
lats_list = np.hstack(lats_list)
shrid_id_list = np.hstack(shrid_id_list)

# Create the final DataFrame with the generated grid coordinates
df = pd.DataFrame({"lon": lons_list, "lat": lats_list, "shrid2": shrid_id_list})

df.to_csv("output_coordinates.csv", index=False)