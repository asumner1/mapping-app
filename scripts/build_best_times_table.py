import pandas as pd

# Read the CSV file
df = pd.read_csv('scripts/national_parks_best_times.csv')

# Create a function to convert the month string into boolean columns
def expand_months(month_str):
    # Initialize all months as False
    months = {month: False for month in ['January', 'February', 'March', 'April', 'May', 'June', 
                                       'July', 'August', 'September', 'October', 'November', 'December']}
    
    # Convert string of numbers to list of integers
    best_months = [int(m.strip()) for m in month_str.split(',')]
    
    # Map month numbers to names and set to True
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    
    for month_num in best_months:
        months[month_map[month_num]] = True
    
    return pd.Series(months)

# Apply the transformation
result = df.join(df['Best Time to Visit'].apply(expand_months))

# Drop the original 'Best Time to Visit' column
result = result.drop('Best Time to Visit', axis=1)

# Save the result to a new CSV file
result.to_csv('scripts/national_parks_best_times_expanded.csv', index=False)
