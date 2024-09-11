import os
import sys
# import http.client, urllib
# import ssl
# import certifi
# from dotenv import load_dotenv

# # Load environment variables (PUSH_NOTIFICATION_TOKEN, PUSH_NOTIFICATION_USER)
# load_dotenv()
# push_token = os.getenv('PUSH_NOTIFICATION_TOKEN')
# push_user = os.getenv('PUSH_NOTIFICATION_USER')

# This ensures the 'package' and 'src' directory is in the path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "package"))

from ebay_data_processor import process_ebay_items, filter_undervalued_items

def main():
    print('Hello!')
    # List of iPhones with model name and price range (in GBP), sorted from iPhone 8 to iPhone 12
    iphones = [
        {'name': 'iPhone 8 64GB', 'min_price': 20, 'max_price': 35},
        {'name': 'iPhone 8 128GB', 'min_price': 30, 'max_price': 60},
        {'name': 'iPhone 8 Plus 64GB', 'min_price': 30, 'max_price': 60},
        {'name': 'iPhone 8 Plus 128GB', 'min_price': 40, 'max_price': 70},

        {'name': 'iPhone X 64GB', 'min_price': 40, 'max_price': 70},
        {'name': 'iPhone X 256GB', 'min_price': 50, 'max_price': 90},

        {'name': 'iPhone XR 64GB', 'min_price': 40, 'max_price': 70},
        {'name': 'iPhone XR 128GB', 'min_price': 60, 'max_price': 100},

        {'name': 'iPhone XS 64GB', 'min_price': 60, 'max_price': 100},
        {'name': 'iPhone XS 256GB', 'min_price': 60, 'max_price': 100},
        {'name': 'iPhone XS Max 64GB', 'min_price': 70, 'max_price': 110},
        {'name': 'iPhone XS Max 256GB', 'min_price': 70, 'max_price': 110},

        {'name': 'iPhone 11 64GB', 'min_price': 70, 'max_price': 110},
        {'name': 'iPhone 11 128GB', 'min_price': 80, 'max_price': 120},

        {'name': 'iPhone 12 64GB', 'min_price': 110, 'max_price': 150},
        {'name': 'iPhone 12 128GB', 'min_price': 120, 'max_price': 160},

        {'name': 'iPhone 12 Pro 128GB', 'min_price': 120, 'max_price': 180},
        {'name': 'iPhone 12 Pro 256GB', 'min_price': 110, 'max_price': 200}
    ]

    all_items = []

    # Iterate over the list of iPhones and fetch eBay items for each one
    for iphone in iphones:
        print(f"Processing {iphone['name']}")
        ebay_items = process_ebay_items(
            iphone['name'], iphone['min_price'], iphone['max_price'], 1000)
        all_items.extend(ebay_items)  # Combine results from each iPhone model

     # Filter out undervalued items based on their condition status
    undervalued_items = filter_undervalued_items(all_items)

    # Display the number and details of undervalued items
    print(f"Number of undervalued items: {len(undervalued_items)}")
    print(undervalued_items)

    # for item in undervalued_items:
    #     # print(f"Check out this {item["Title"]}, going for {item["Price"]} GBP : {item["URL"]}")
    #     # Use certifi's certificate bundle
    #     context = ssl.create_default_context(cafile=certifi.where())

    #     conn = http.client.HTTPSConnection("api.pushover.net:443", context=context)
    #     conn.request("POST", "/1/messages.json",
    #         urllib.parse.urlencode({
    #             "token": push_token,
    #             "user": push_user,
    #             "message": f"Check out this {item["Title"]}, going for {item["Price"]} GBP : {item["URL"]}",
    #         }), { "Content-type": "application/x-www-form-urlencoded" })

    #     response = conn.getresponse()
    #     print(response.status, response.reason)

if __name__ == "__main__":
    main()
