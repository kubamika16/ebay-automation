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
        {'name': 'iPhone 8 64GB', 'min_price': 0, 'max_price': 435},
        {'name': 'iPhone 8 128GB', 'min_price': 10, 'max_price': 460},
        {'name': 'iPhone 8 Plus 64GB', 'min_price': 10, 'max_price': 460},
        {'name': 'iPhone 8 Plus 128GB', 'min_price': 20, 'max_price': 470},
        {'name': 'iPhone X 64GB', 'min_price': 20, 'max_price': 470},
        {'name': 'iPhone X 256GB', 'min_price': 30, 'max_price': 490},
        {'name': 'iPhone XR 64GB', 'min_price': 20, 'max_price': 470},
        {'name': 'iPhone XR 128GB', 'min_price': 40, 'max_price': 500},
        {'name': 'iPhone XS 64GB', 'min_price': 40, 'max_price': 500},
        {'name': 'iPhone XS 256GB', 'min_price': 40, 'max_price': 500},
        {'name': 'iPhone XS Max 64GB', 'min_price': 50, 'max_price': 510},
        {'name': 'iPhone XS Max 256GB', 'min_price': 50, 'max_price': 510},
        {'name': 'iPhone 11 64GB', 'min_price': 50, 'max_price': 510},
        {'name': 'iPhone 11 128GB', 'min_price': 60, 'max_price': 520},
        {'name': 'iPhone 12 64GB', 'min_price': 90, 'max_price': 550},
        {'name': 'iPhone 12 128GB', 'min_price': 100, 'max_price': 560},
        {'name': 'iPhone 12 Pro 128GB', 'min_price': 100, 'max_price': 580},
        {'name': 'iPhone 12 Pro 256GB', 'min_price': 90, 'max_price': 600}
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
