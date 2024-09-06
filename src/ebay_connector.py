import os
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from utils import clean_description

# Load environment variables from .env file
load_dotenv()
access_token = os.getenv('EBAY_ACCESS_TOKEN')
ebay_app_id = os.getenv('EBAY_APP_ID')

def search_items(item_name, min_price, max_price, time_limit_minutes):
    try:
        api = Finding(appid=ebay_app_id, config_file=None)

        # Get the current time and calculate the time limit
        current_time = datetime.now(timezone.utc)
        time_limit = current_time - timedelta(minutes=time_limit_minutes)

        request = {
            'keywords': item_name,
            'itemFilter': [
                {'name': 'MinPrice', 'value': min_price, 'paramName': 'Currency', 'paramValue': 'GBP'},
                {'name': 'MaxPrice', 'value': max_price, 'paramName': 'Currency', 'paramValue': 'GBP'},
                {'name': 'Condition', 'value': 'Used'},
                {'name': 'LocatedIn', 'value': 'GB'}
            ],
            'sortOrder': 'StartTimeNewest',
        }

        response = api.execute('findItemsAdvanced', request)
        items = response.reply.searchResult.item

        # Loop through the results and filter by startTime
        for item in items:
            # Ensure item_start_time is in UTC (offset-aware)
            item_start_time = item.listingInfo.startTime

            if item_start_time.tzinfo is None:
                item_start_time = item_start_time.replace(tzinfo=timezone.utc)

           
            # If the item was listed within the last `time_limit_minutes`
            if item_start_time >= time_limit:
                print(f"ID: {item.itemId}")
                print(f"Title: {item.title}")
                print(f"Description: {get_item_details(item.itemId)}")
                print(f"URL: {item.viewItemURL}")
                print(f"Price: {item.sellingStatus.currentPrice.value}")
                print(f"Image URL: {item.galleryURL}")
                print("-" * 40)

    except ConnectionError as e:
        print(f"Error: {e}")


def get_item_details(item_id):
    """Fetch details of an item from eBay by its item ID"""
    url = f"https://api.ebay.com/buy/browse/v1/item/v1|{item_id}|0"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    response = requests.get(url, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        json_response = response.json()  # Parse the response in JSON format
        
        # Check if 'description' exists in the response
        if 'description' in json_response:
            raw_description = json_response['description']
            cleaned_description = clean_description(raw_description)
            return cleaned_description
        else:
            return "Description not found."
    else:
        return f"Error: {response.status_code}, {response.text}"

# Example function call
if __name__ == "__main__":
    search_items('iPhone 12', 150, 200, 10)
    # print(get_item_details(326164639406))
