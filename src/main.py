import os
import sys


# This ensures the 'package' and 'src' directory is in the path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "package"))

from src.ebay_data_processor import process_ebay_items, filter_undervalued_items

def main(event, context):
    print('Hello!')
    # List of iPhones with model name and price range (in GBP), sorted from iPhone 8 to iPhone 12
    iphones = [
        {'name': 'iPhone 8 64GB', 'min_price': 0, 'max_price': 235},
        {'name': 'iPhone 8 128GB', 'min_price': 10, 'max_price': 260},
        {'name': 'iPhone 8 Plus 64GB', 'min_price': 10, 'max_price': 260},
        {'name': 'iPhone 8 Plus 128GB', 'min_price': 20, 'max_price': 270},
        {'name': 'iPhone X 64GB', 'min_price': 20, 'max_price': 270},
        {'name': 'iPhone X 256GB', 'min_price': 30, 'max_price': 290},
        {'name': 'iPhone XR 64GB', 'min_price': 20, 'max_price': 270},
        {'name': 'iPhone XR 128GB', 'min_price': 40, 'max_price': 300},
        {'name': 'iPhone XS 64GB', 'min_price': 40, 'max_price': 300},
        {'name': 'iPhone XS 256GB', 'min_price': 40, 'max_price': 300},
        {'name': 'iPhone XS Max 64GB', 'min_price': 50, 'max_price': 310},
        {'name': 'iPhone XS Max 256GB', 'min_price': 50, 'max_price': 310},
        {'name': 'iPhone 11 64GB', 'min_price': 50, 'max_price': 310},
        {'name': 'iPhone 11 128GB', 'min_price': 60, 'max_price': 320},
        {'name': 'iPhone 12 64GB', 'min_price': 90, 'max_price': 350},
        {'name': 'iPhone 12 128GB', 'min_price': 100, 'max_price': 360},
        {'name': 'iPhone 12 Pro 128GB', 'min_price': 100, 'max_price': 380},
        {'name': 'iPhone 12 Pro 256GB', 'min_price': 90, 'max_price': 400}
    ]


    all_items = []

    # Iterate over the list of iPhones and fetch eBay items for each one
    for iphone in iphones:
        print(f"Processing {iphone['name']}")
        ebay_items = process_ebay_items(
            iphone['name'], iphone['min_price'], iphone['max_price'], 100)
        all_items.extend(ebay_items)  # Combine results from each iPhone model

     # Filter out undervalued items based on their condition status
    undervalued_items = filter_undervalued_items(all_items)

    # Display the number and details of undervalued items
    print(f"Number of undervalued items: {len(undervalued_items)}")
    print(undervalued_items)


if __name__ == "__main__":
    main()
