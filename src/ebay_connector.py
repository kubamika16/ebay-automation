import os
import pytz
import requests
import base64
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from utils import clean_description


from openai_interaction import analyze_item_condition

# Load environment variables (EBAY_ACCESS_TOKEN, EBAY_APP_ID)
load_dotenv()
# access_token = os.getenv('EBAY_ACCESS_TOKEN')
refresh_token = os.getenv('REFRESH_TOKEN')
client_secret = os.getenv('CLIENT_SECRET')
ebay_app_id = os.getenv('EBAY_APP_ID')


def refresh_access_token():
    """Refresh the eBay API access token using the refresh token."""
    # Encode client credentials
    basic_auth = base64.b64encode(f"{ebay_app_id}:{client_secret}".encode()).decode()

    # Set headers and body for the request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {basic_auth}'
    }

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'scope': 'https://api.ebay.com/oauth/api_scope'
    }

    # Make the POST request to refresh the access token
    response = requests.post('https://api.ebay.com/identity/v1/oauth2/token', headers=headers, data=data)

    # Handle the response
    if response.status_code == 200:
        new_access_token = response.json().get('access_token')
        # print(f"New Access Token: {new_access_token}")
        return new_access_token
    else:
        print(f"Failed to refresh token: {response.status_code} - {response.text}")
        return None

access_token = refresh_access_token()

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
                {'name': 'MinPrice', 'value': min_price,
                    'paramName': 'Currency', 'paramValue': 'GBP'},
                {'name': 'MaxPrice', 'value': max_price,
                    'paramName': 'Currency', 'paramValue': 'GBP'},
                {'name': 'Condition', 'value': 'Used'},
                {'name': 'LocatedIn', 'value': 'GB'},
                # Only include Buy It Now listings
                {'name': 'ListingType', 'value': 'FixedPrice'}
            ],
            'sortOrder': 'StartTimeNewest',  # Sort by newest listings
            # 'listingType': ['FixedPrice']  # Only retrieve Buy It Now listings
        }

        # Execute the search and return the found items
        response = api.execute('findItemsAdvanced', request)

        # Debugging: Print the entire response structure
        # print(response.reply)

        # Check if 'searchResult' exists and if it contains items
        if hasattr(response.reply, 'searchResult') and hasattr(response.reply.searchResult, 'item'):
            return response.reply.searchResult.item
        else:
            return []

    except ConnectionError as e:
        print(f"Error: {e}")
        return []


# # Example function call
# if __name__ == "__main__":
#     fetch_items_from_ebay('iPhone 12 64GB', 150, 300, 60)
