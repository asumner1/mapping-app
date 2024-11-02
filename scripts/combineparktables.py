import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Read the CSV files
parks_with_urls = pd.read_csv('scripts/us_national_parks_with_urls.csv')
cleaned_parks = pd.read_csv('scripts/cleaned_parks_table.csv')

def combine_descriptions(row):
    """Combine descriptions from both sources, avoiding redundancy."""
    desc1 = row['Description_x'] if pd.notna(row['Description_x']) else ''
    desc2 = row['Description_y'] if pd.notna(row['Description_y']) else ''
    
    # If both descriptions exist, combine them
    if desc1 and desc2:
        # Remove potential period at the end of first description
        desc1 = desc1.rstrip('.')
        return f"{desc1}. {desc2}"
    # Return whichever description exists
    return desc1 or desc2

# Create a mapping dictionary using fuzzy matching
park_mapping = {}
for park_name in parks_with_urls['National Park']:
    match = process.extractOne(park_name, cleaned_parks['Name'], scorer=fuzz.ratio)
    if match[1] >= 80:  # Only match if similarity score is 80 or higher
        park_mapping[park_name] = match[0]

# Create a mapping series
mapping_series = pd.Series(park_mapping)

# Map the names to match cleaned_parks format
parks_with_urls['Matched_Name'] = parks_with_urls['National Park'].map(mapping_series)

# Merge the dataframes
merged_df = pd.merge(
    parks_with_urls,
    cleaned_parks,
    left_on='Matched_Name',
    right_on='Name',
    how='outer'
)

# Combine descriptions
merged_df['Combined_Description'] = merged_df.apply(combine_descriptions, axis=1)

# Select and rename columns for final output
final_df = merged_df[[
    'Name',  # Park name from cleaned_parks
    'Combined_Description',
    'Location',
    'Date established as park[12]',
    'Area (2023)[8]',
    'Recreation visitors (2022)[11]',
    'Latitude',
    'Longitude',
    'AllTrails URL'
]].copy()

# Rename columns for clarity
final_df = final_df.rename(columns={
    'Date established as park[12]': 'Established',
    'Area (2023)[8]': 'Area',
    'Recreation visitors (2022)[11]': 'Annual_Visitors',
    'Combined_Description': 'Description'
})

# Save to CSV
final_df.to_csv('scripts/combined_parks_data.csv', index=False)