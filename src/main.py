from ebay_connector import search_items
from openai_interaction import analyze_item_condition

def main():
    ebay_items = search_items('iPhone 12', 200, 300, 60)
    print(len(ebay_items))

    # Main loop that processes the ebay items
    def process_items_with_gpt(ebay_items):
        for ebay_item in ebay_items:
            description = ebay_item['Description']  # Get the description
            condition_status = analyze_item_condition(description)  # Analyze the description with GPT
            
            # Add the condition result as a new key in the ebay_item dictionary
            ebay_item['Condition Status'] = condition_status
            print(f"ID: {ebay_item["ID"]}")
            print(f"Title: {ebay_item["Title"]}")
            print(f"Description: {ebay_item["Description"]}")
            print(f"Condition Status: {ebay_item["Condition Status"]}")
            print(f"URL: {ebay_item["URL"]}")
            print(f"Price: {ebay_item["Price"]}")
            print(f"Image URL: {ebay_item["Image URL"]}")
            print("-" * 40)
        return ebay_items  # Now each item includes a 'Condition Status'

    process_items_with_gpt(ebay_items)

if __name__ == "__main__":
    main()