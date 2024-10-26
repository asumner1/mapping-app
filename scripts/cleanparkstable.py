import pandas as pd
import re

def load_csv_to_dataframe(file_path):
    """
    Load a CSV file into a pandas DataFrame.
    
    Args:
    file_path (str): Path to the CSV file.
    
    Returns:
    pandas.DataFrame: DataFrame containing the CSV data.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded {file_path} into a DataFrame.")
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except pd.errors.EmptyDataError:
        print(f"Error: The file at {file_path} is empty.")
    except pd.errors.ParserError:
        print(f"Error: Unable to parse the file at {file_path}. Make sure it's a valid CSV.")
    return None


df = load_csv_to_dataframe('scraped_tables/table_1.csv')

# Remove the Image column
df = df.drop('Image', axis=1)

# Clean the Name column
df['Name'] = df['Name'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]+$', '', str(x)).strip())

# Clean the Location column
def clean_location(loc):
    # Split on forward slash and keep the second part
    parts = loc.split('/')
    if len(parts) > 1:
        loc = parts[1]
    # Keep only alphanumeric characters, period, and regular space
    cleaned = re.sub(r'[^a-zA-Z0-9.\s]+', '', loc)
    # Replace any non-breaking spaces with regular spaces
    cleaned = cleaned.replace('\xa0', ' ')
    cleaned = cleaned.strip()

    parts = cleaned.split()
    for i in range(len(parts)):
        if parts[i].endswith('S') or parts[i].endswith('W'):
            parts[i] = '-' + parts[i]
        parts[i] = parts[i][:-1]
    cleaned = f"{parts[0]},{parts[1]}"
    
    return cleaned

df['Location'] = df['Location'].apply(clean_location)

df['Latitude'] = df.apply(lambda x: float(x['Location'].split(',')[0]), axis=1)
df['Longitude'] = df.apply(lambda x: float(x['Location'].split(',')[1]), axis=1)

# Print the resulting dataframe
print(df.to_string())

# Save the cleaned dataframe as a CSV file
df.to_csv('cleaned_parks_table.csv', index=False)
