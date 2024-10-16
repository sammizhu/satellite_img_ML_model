import pandas as pd

# Load the CSV files
strategy1_features = pd.read_csv('/Users/sammizhu/SUPER/strategy2/strategy1_features_p1.csv')
strategy2_features = pd.read_csv('/Users/sammizhu/SUPER/strategy2/strategy2_features.csv')
shrid2 = pd.read_csv('/Users/sammizhu/SUPER/strategy2/shrid2.csv')

# Compare Lat/Lon between strategy1_features and strategy2_features
# Find matching rows by merging on Lat and Lon
matches = pd.merge(strategy2_features, strategy1_features, on=['Lat', 'Lon'])

# For the matching rows, look for those Lat and Lon in shrid2 and return only columns from shrid2
matches_with_shrid2 = pd.merge(matches, shrid2, on=['Lat', 'Lon'])[shrid2.columns]

# Find rows in strategy2_features that do not match with strategy1_features by Lat/Lon
non_matches = strategy2_features[~strategy2_features.set_index(['Lat', 'Lon']).index.isin(matches.set_index(['Lat', 'Lon']).index)]

# For the non-matching rows, find corresponding rows in shrid2 by Lat/Lon and return only columns from shrid2
non_matches_with_shrid2 = pd.merge(non_matches, shrid2, on=['Lat', 'Lon'])[shrid2.columns]

# Save the results to external CSV files
matches_with_shrid2.to_csv('/Users/sammizhu/SUPER/strategy2/matches_shrid2.csv', index=False)  # Contains matching rows from shrid2
non_matches_with_shrid2.to_csv('/Users/sammizhu/SUPER/strategy2/non_matches_shrid2.csv', index=False)  # Contains non-matching rows from shrid2

print("CSV files have been created: 'matches_shrid2.csv' and 'non_matches_shrid2.csv'")