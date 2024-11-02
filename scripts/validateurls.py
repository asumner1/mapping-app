import requests
import time
import random
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from typing import List, Dict
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class URLValidator:
    def __init__(self):
        # Initialize fake user agent generator
        self.ua = UserAgent()
        
        # Configure session with retries and backoff
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def get_headers(self) -> Dict:
        """Generate random headers to appear more human-like"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
        }

    def validate_url(self, url: str) -> Dict:
        """Validate a single URL and return its status"""
        try:
            # Add random delay between requests (1-3 seconds)
            time.sleep(random.uniform(1, 3))
            
            response = self.session.head(
                url,
                headers=self.get_headers(),
                timeout=10,
                allow_redirects=True
            )
            
            return {
                'url': url,
                'status': response.status_code,
                'valid': response.status_code == 200,
                'error': None
            }
            
        except requests.RequestException as e:
            return {
                'url': url,
                'status': None,
                'valid': False,
                'error': str(e)
            }

def validate_urls(urls: List[str], max_workers: int = 3) -> List[Dict]:
    """
    Validate a list of URLs with concurrent execution and rate limiting
    
    Args:
        urls: List of URLs to validate
        max_workers: Maximum number of concurrent workers
    
    Returns:
        List of dictionaries containing validation results
    """
    validator = URLValidator()
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(validator.validate_url, urls))
    
    return results

if __name__ == "__main__":
    # Example usage
    test_urls = [
        "https://www.google.com",
        "https://www.github.com",
        "https://www.thisisaprobablybrokenlinkxyz.com",
    ]
    
    results = validate_urls(test_urls)
    
    for result in results:
        if result['valid']:
            logger.info(f"✅ {result['url']} is valid (Status: {result['status']})")
        else:
            logger.error(f"❌ {result['url']} is invalid {f'(Error: {result[\"error\"]})' if result['error'] else ''}")
