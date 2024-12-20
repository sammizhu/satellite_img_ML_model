import pandas as pd

df_a = pd.read_csv("")  # features output files
df_b = pd.read_csv("")  # coordinate files with the lat, lon, and shird2
output_file =  "" #path name for file that you want to store it to

# Merge the files based on desired columns 
merged_df = pd.merge(df_a, df_b, on=[], how='inner') #fill in on=[]

# Reorder columns to match the desired output
columns = [] + [col for col in merged_df.columns if col not in []] #fill in []
merged_df = merged_df[columns]

# Save the merged data to the output file
merged_df.to_csv(output_file, index=False)
print(f"Successfully merged and saved to {output_file}")

