import os
import pytz
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from utils import clean_description


from openai_interaction import analyze_item_condition

# Load environment variables (EBAY_ACCESS_TOKEN, EBAY_APP_ID)
load_dotenv()
access_token = os.getenv('EBAY_ACCESS_TOKEN')
ebay_app_id = os.getenv('EBAY_APP_ID')

def get_item_details(item_id):
    """Fetch detailed information about a specific eBay item."""
    url = f"https://api.ebay.com/buy/browse/v1/item/v1|{item_id}|0"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    # Make a request to eBay API for item details
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        json_response = response.json()
        
        # If description is available, clean it
        if 'description' in json_response:
            raw_description = json_response['description']
            cleaned_description = clean_description(raw_description)
            return cleaned_description
        else:
            return "Description not found."
    else:
        return f"Error: {response.status_code}, {response.text}"

def fetch_items_from_ebay(item_name, min_price, max_price, time_limit_minutes):
    """Search eBay for items based on keywords, price range, and condition."""
    try:
        api = Finding(appid=ebay_app_id, config_file=None)

        # Build request payload for eBay API search
        request = {
            'keywords': item_name,
            'itemFilter': [
                {'name': 'MinPrice', 'value': min_price, 'paramName': 'Currency', 'paramValue': 'GBP'},
                {'name': 'MaxPrice', 'value': max_price, 'paramName': 'Currency', 'paramValue': 'GBP'},
                {'name': 'Condition', 'value': 'Used'},
                {'name': 'LocatedIn', 'value': 'GB'}
            ],
            'sortOrder': 'StartTimeNewest', # Sort by newest listings
        }

        # Execute the search and return the found items
        response = api.execute('findItemsAdvanced', request)
        return response.reply.searchResult.item

    except ConnectionError as e:
        print(f"Error: {e}")
        return []

# Example function call
if __name__ == "__main__":
    fetch_items_from_ebay('iPhone 12 64GB', 150, 300, 60)












