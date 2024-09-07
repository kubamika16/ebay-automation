from ebay_data_processor import process_ebay_items, filter_undervalued_items

def main():
    # List of iPhones with model name and price range (in GBP)
    iphones = [
        {'name': 'iPhone 12 64GB', 'min_price': 150, 'max_price': 200},
        {'name': 'iPhone 12 128GB', 'min_price': 170, 'max_price': 250},
        {'name': 'iPhone 11 64GB', 'min_price': 130, 'max_price': 180},
        {'name': 'iPhone 11 128GB', 'min_price': 150, 'max_price': 230},
        {'name': 'iPhone 13 128GB', 'min_price': 300, 'max_price': 400},
        {'name': 'iPhone 13 256GB', 'min_price': 350, 'max_price': 450},
        {'name': 'iPhone 12 Pro 128GB', 'min_price': 250, 'max_price': 350},
        {'name': 'iPhone 12 Pro 256GB', 'min_price': 300, 'max_price': 400},
        {'name': 'iPhone 13 Pro 128GB', 'min_price': 450, 'max_price': 550},
        {'name': 'iPhone 13 Pro 256GB', 'min_price': 500, 'max_price': 600},
        # Add more models as needed
    ]

    all_items = []

     # Iterate over the list of iPhones and fetch eBay items for each one
    for iphone in iphones:
        print(f"Processing {iphone['name']}")
        ebay_items = process_ebay_items(iphone['name'], iphone['min_price'], iphone['max_price'], 60)
        all_items.extend(ebay_items) # Combine results from each iPhone model

     # Filter out undervalued items based on their condition status
    undervalued_items = filter_undervalued_items(all_items)

    # Display the number and details of undervalued items
    print(f"Number of undervalued items: {len(undervalued_items)}")
    print(undervalued_items)

if __name__ == "__main__":
    main()