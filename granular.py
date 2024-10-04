import pandas as pd
import numpy as np

# Read the CSV file into a DataFrame
shrid = pd.read_csv("")

# Round and adjust the coordinates
shrid["min_lat_round"] = shrid["min_lat"].round(2) + .005
shrid["max_lat_round"] = shrid["max_lat"].round(2) - .005
shrid["min_lon_round"] = shrid["min_lon"].round(2) + .005
shrid["max_lon_round"] = shrid["max_lon"].round(2) - .005

# Initialize lists to store the results
lons_list = []
lats_list = []
shrid_id_list = []
id_count_list = []

# Iterate over each row in the DataFrame to generate a grid of coordinates
for i, row in shrid.iterrows():
    x_range = np.arange(row["min_lon_round"], row["max_lon_round"] + 0.01, 0.01)
    y_range = np.arange(row["min_lat_round"], row["max_lat_round"] + 0.01, 0.01)
    x_grid, y_grid = np.meshgrid(x_range, y_range)

    lons = x_grid.flatten()
    lats = y_grid.flatten()

    # Filter both lons and lats based on the current row's min/max bounds
    # Ensures no out-of-bound region errors 
    valid_indices = (lons >= row["min_lon"]) & (lons <= row["max_lon"]) & \
                    (lats >= row["min_lat"]) & (lats <= row["max_lat"])
    
    lons_filtered = lons[valid_indices]
    lats_filtered = lats[valid_indices]

    # If filtered arrays are not empty, append the corresponding shrid2 values
    if len(lons_filtered) > 0 and len(lats_filtered) > 0:
        shrid_id = np.full(len(lons_filtered), row["shrid2"])
        id_count = np.full(len(lons_filtered), row["Unnamed: 0"])

        lons_list.append(lons_filtered)
        lats_list.append(lats_filtered)
        shrid_id_list.append(shrid_id)
        id_count_list.append(id_count)

# Combine all the individual lists into single flat arrays
lons_list = np.hstack(lons_list)
lats_list = np.hstack(lats_list)
shrid_id_list = np.hstack(shrid_id_list)
id_count_list = np.hstack(id_count_list)

# Create the final DataFrame with the generated grid coordinates
df = pd.DataFrame({"Unnamed: 0": id_count_list, "shrid2": shrid_id_list, "Lon": lons_list, "Lat": lats_list}) 

# Restrict the number of rows per CSV file to a maximum of 100,000
chunk_size = 100000
total_rows = df.shape[0]
num_chunks = (total_rows // chunk_size) + 1

# Save the DataFrame to multiple CSV files if necessary
for i in range(num_chunks):
    start_row = i * chunk_size
    end_row = min((i + 1) * chunk_size, total_rows)
    
    chunk_df = df.iloc[start_row:end_row]
    chunk_filename = f"file_coordinates_{i+1}.csv"
    chunk_df.to_csv(chunk_filename, index=False, float_format="%.3f")
    
    print(f"Saved {chunk_filename} with rows {start_row} to {end_row - 1}")