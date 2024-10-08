import os
import sys

# This ensures the 'package' and 'src' directory is in the path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "package"))

from src.utils import push_notification_sender
from src.ebay_data_processor import process_ebay_items, filter_undervalued_items

def main(event, context):
    time_limit = 5
    print(f"-----THIS FUNCTION RUNS EVERY {time_limit} MINUTES AND CHECK ITEMS FROM LAST {time_limit} MINUTES-----")

    # List of Apple products with model name and price range (in GBP)
    apple_products = [
        #IPHONES
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
        {'name': 'iPhone 12 Pro 256GB', 'min_price': 110, 'max_price': 200},

        {'name': 'iPhone 13 128GB', 'min_price': 200, 'max_price': 250},
        {'name': 'iPhone 13 256GB', 'min_price': 200, 'max_price': 270},
        {'name': 'iPhone 13 Mini 128GB', 'min_price': 150, 'max_price': 200},
        {'name': 'iPhone 13 Mini 256GB', 'min_price': 150, 'max_price': 230},
        {'name': 'iPhone 13 Pro 128GB', 'min_price': 300, 'max_price': 330},
        {'name': 'iPhone 13 Pro 256GB', 'min_price': 300, 'max_price': 350},
        {'name': 'iPhone 13 Pro Max 128GB', 'min_price': 240, 'max_price': 290},
        {'name': 'iPhone 13 Pro Max 256GB', 'min_price': 250, 'max_price': 350},

        {'name': 'iPhone 14 128GB', 'min_price': 300, 'max_price': 350},
        {'name': 'iPhone 14 256GB', 'min_price': 300, 'max_price': 350},
        {'name': 'iPhone 14 Plus 128GB', 'min_price': 280, 'max_price': 330},
        {'name': 'iPhone 14 Plus 256GB', 'min_price': 280, 'max_price': 350},
        {'name': 'iPhone 14 Pro 128GB', 'min_price': 380, 'max_price': 480},
        {'name': 'iPhone 14 Pro 256GB', 'min_price': 400, 'max_price': 500},
        {'name': 'iPhone 14 Pro Max 128GB', 'min_price': 450, 'max_price': 500},
        {'name': 'iPhone 14 Pro Max 256GB', 'min_price': 450, 'max_price': 540},

        #IPADS
        # {'name': 'iPad Air 4th Gen 64GB', 'min_price': 150, 'max_price': 200},
        # {'name': 'iPad Air 4th Gen 256GB', 'min_price': 200, 'max_price': 280},
        # {'name': 'iPad 9th Gen 64GB', 'min_price': 120, 'max_price': 180},
        # {'name': 'iPad 9th Gen 256GB', 'min_price': 150, 'max_price': 200},
        # {'name': 'iPad Pro 2018 64GB', 'min_price': 150, 'max_price': 220},
        # {'name': 'iPad Pro 2018 256GB', 'min_price': 180, 'max_price': 240},
        # {'name': 'iPad Mini 6th Gen 64GB', 'min_price': 180, 'max_price': 240},
        # {'name': 'iPad Mini 6th Gen 256GB', 'min_price': 220, 'max_price': 300},
    ]

    all_items = []

    # Iterate over the list of Apple products and fetch eBay items for each one. Last argument is about timestamp of the data (5 minutes means that data will be collected from eBay from last 5 minutes)
    for apple_product in apple_products:
        print(f"Processing {apple_product['name']}")
        ebay_items = process_ebay_items(apple_product['name'], apple_product['min_price'], apple_product['max_price'], time_limit)

        # Add price range to each eBay item
        price_range_message = f"£{apple_product['min_price']} - £{apple_product['max_price']}"
        for item in ebay_items:
            item['Price Range'] = price_range_message

        all_items.extend(ebay_items)  # Combine results from each Apple product model

     # Filter out undervalued items based on their condition status
    undervalued_items = filter_undervalued_items(all_items)

    # Display the number and details of undervalued items
    print(f"Number of undervalued items ({len(undervalued_items)}): {undervalued_items}")

    # Send notifications for undervalued items
    for item in undervalued_items:
        try:
            message = f"Undervalued item: <b>{item['Title']}</b>\nPrice: £{item['Price']} (within range of {item['Price Range']})\n<a href='{item['URL']}'>Check it out!</a>"
            print(f"Sending notification: {message}")
            push_notification_sender(message)
        except Exception as e:
            print(f"Failed to send notification for item {item['ID']}: {str(e)}")


if __name__ == "__main__":
    main()
