
import requests
import random
from dotenv import load_dotenv
import os

load_dotenv()

def get_proxy():
    """
    Gets a proxy from a service. This example uses ScraperAPI.
    For a free proxy list, you'd shuffle a list and check if alive.
    """
    SCRAPERAPI_KEY = os.getenv('SCRAPERAPI_KEY')
    if SCRAPERAPI_KEY:
        # Format for ScraperAPI (a popular, paid, reliable service)
        proxy_url = f"http://scraperapi:{SCRAPERAPI_KEY}@proxy-server.scraperapi.com:8001"
        return {'http': proxy_url, 'https': proxy_url}
    else:
        # Fallback to a free, unreliable proxy list (for testing only)
        free_proxies = [
            '103.123.64.234:3128',
            '200.105.209.250:80',
            # ... get a fresh list from sites like https://free-proxy-list.net/
        ]
        if free_proxies:
            chosen = random.choice(free_proxies)
            return {'http': f'http://{chosen}', 'https': f'http://{chosen}'}
        return None