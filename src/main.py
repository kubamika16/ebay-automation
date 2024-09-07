from ebay_connector import search_items

def main():
    # Result of returned items: (item name, min price, max price, time range of how many minutes ago item was posted from now on)
    ebay_items = search_items('iPhone 12', 150, 200, 200)

    # Number of filtered items with GPT decision about description (GOOD CONDITION / BAD CONDITION)
    print(f"Number of filtered items: {len(ebay_items)}")
    print(ebay_items)

    undervalued_list = []
    for ebay_item in ebay_items:
        if ebay_item["Condition Status"] == "GOOD CONDITION":
            undervalued_list.append(ebay_item)

    print(f"Number of undervalued items: {len(undervalued_list)}")
    print(f"Undervalued List: {undervalued_list}")

    # Result of dictionary with items 

if __name__ == "__main__":
    main()