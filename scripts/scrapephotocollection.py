import requests
import json
import time

def fetch_nps_photos(max_pages=None, search_params=None):
    """
    Iterates through search results from NPS photo gallery
    
    Args:
        max_pages (int, optional): Maximum number of pages to retrieve. If None, retrieves all pages.
        search_params (dict, optional): Additional search parameters to filter results.
    """
    base_url = "https://www.nps.gov/npgallery/api/search/execute"
    
    # Basic search template
    search_template = {
        "page": 1,
        "pageSize": 100,  # Maximum allowed per page
        "sortTerms": [
            {"Term": "Rating", "Ascending": False},
            {"Term": "CategoryScenic", "Ascending": False},
            {"Term": "CategoryHistoric", "Ascending": False},
            {"Term": "SubmittedDateTime", "Ascending": False}
        ]
    }

    # Add any additional search parameters
    if search_params:
        search_template.update(search_params)

    headers = {
        'Content-Type': 'application/json'
    }

    pages_retrieved = 0
    
    while True:
        try:
            response = requests.post(base_url, 
                                  json=search_template,
                                  headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            # Process results
            for result in data['Results']:
                yield result['Asset']
            
            pages_retrieved += 1
            
            # Check if we've reached the max pages limit
            if max_pages and pages_retrieved >= max_pages:
                print(f"Reached requested limit of {max_pages} pages")
                break
                
            # Check if we've reached the end of all results
            if search_template['page'] >= data['PageCount']:
                print(f"Reached end of results at page {pages_retrieved}")
                break
                
            # Move to next page
            search_template['page'] += 1
            
            # Be nice to their servers
            time.sleep(1)
            
        except Exception as e:
            print(f"Error fetching page {search_template['page']}: {e}")
            break

# Example usage
if __name__ == "__main__":
    # Search for maps with specific keywords
    search_params = {
        "Operand": {
            "LeftOperand": {
                "Term": "keyword",
                "Attribute": "Park Map - ",
                "OperandType": "containsText"
            },
            "RightOperand": {
                "Term": "keyword",
                "Attribute": "National Park",
                "OperandType": "containsText"
            },
            "Operator": "AND"
        }
    }
    
    # Only fetch first 2 pages as an example
    for photo in fetch_nps_photos(max_pages=2, search_params=search_params):
        print(f"Title: {photo['Title']}")
        print(f"Asset ID: {photo['AssetID']}")
        print(f"URL: https://www.nps.gov/npgallery/GetAsset/{photo['AssetID']}/proxy/lores")
        print("---")