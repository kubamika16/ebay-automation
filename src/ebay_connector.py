import os
import requests
from dotenv import load_dotenv
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from bs4 import BeautifulSoup  # to clean the HTML in descriptions

# Load environment variables from .env file
load_dotenv()
access_token = os.getenv('EBAY_ACCESS_TOKEN')
ebay_app_id = os.getenv('EBAY_APP_ID')

def search_items(itemName):
    """Search for items with specific filters using eBay Finding API"""
    try:
        api = Finding(appid=ebay_app_id, config_file=None)
        request = {
            'keywords': itemName,
            'itemFilter': [
                {'name': 'MaxPrice', 'value': 100},
                {'name': 'Condition', 'value': 'Used'},  # You can adjust this as needed
                {'name': 'ListingType', 'value': 'FixedPrice'},  # For Buy It Now listings
            ],
            'outputSelector': 'PictureURLLarge'  # To include image URLs
        }
        response = api.execute('findItemsAdvanced', request)
        items = response.reply.searchResult.item
        for item in items:
                    print(f"ID: {item.itemId}")
                    print(f"Title: {item.title}")
                    print(f"Description: {get_item_details(item.itemId)}")
                    print(f"URL: {item.viewItemURL}")  # URL for manual inspection
                    print(f"Price: {item.sellingStatus.currentPrice.value}")
                    print(f"Image URL: {item.galleryURL}")  # Image for analysis
                    print("-" * 40)
    except ConnectionError as e:
        print(f"Error: {e}")

def clean_description(description):
    """Cleans HTML from the description using BeautifulSoup"""
    if description:
        soup = BeautifulSoup(description, 'html.parser')
        return soup.get_text(separator="\n").strip()
    return "No description available."


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
    print(search_items('iPhone 11'))
    print(get_item_details(326164639406))
