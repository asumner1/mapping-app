import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_tables(url):
    if url == "" or url == None:
        print("No URL provided")
        return
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all table elements
        tables = soup.find_all('table')
        
        # Create a directory to store CSV files
        os.makedirs('scraped_tables', exist_ok=True)
        
        # Iterate through each table
        for i, table in enumerate(tables):
            # Convert the table to a pandas DataFrame
            df = pd.read_html(str(table))[0]
            
            # Generate a filename for the CSV
            filename = f'scraped_tables/table_{i+1}.csv'
            
            # Save the DataFrame as a CSV file
            df.to_csv(filename, index=False)
            
            print(f"Table {i+1} saved as {filename}")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


url = input("Enter the URL of the webpage to scrape: ")
scrape_tables(url)
