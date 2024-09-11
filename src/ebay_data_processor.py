import pytz
from ebay_connector import fetch_items_from_ebay, get_item_details
from openai_interaction import analyze_item_condition
from utils import clean_description
from datetime import datetime, timedelta, timezone


def process_ebay_items(item_name, min_price, max_price, time_limit_minutes):
    """Process eBay items based on search criteria and filter by time listed."""
    items = fetch_items_from_ebay(
        item_name, min_price, max_price, time_limit_minutes)
    #  print(items)
    relevant_items = []
    gpt4o_interaction_counter = 0

    # Get the UK timezone
    uk_timezone = pytz.timezone('Europe/London')

    # Loop through each item and process only the ones listed within the time limit
    for item in items:
        # print(item)
        # Get the item start time and convert it to UK time
        item_start_time = item.listingInfo.startTime

        # print(item_start_time)
        # Ensure the start time is in UTC
        if item_start_time.tzinfo is None:
            item_start_time = item_start_time.replace(tzinfo=timezone.utc)

        # Convert the item start time to UK time
        item_start_time_uk = item_start_time.astimezone(uk_timezone)

        # Calculate the current time in UK time and the time limit
        uk_local_time = datetime.now(timezone.utc).astimezone(uk_timezone)
        time_limit = uk_local_time - timedelta(minutes=time_limit_minutes)

        if item_start_time_uk >= time_limit:

            # Get item description and analyze condition
            description = clean_description(get_item_details(item.itemId))
            condition_status = analyze_item_condition(description, item.title)
            gpt4o_interaction_counter = gpt4o_interaction_counter + 1

            # Store relevant details about the item
            relevant_items.append({
                'ID': item.itemId,
                'Title': item.title,
                'Description': description,
                'Condition Status': condition_status,
                'URL': item.viewItemURL,
                'Price': item.sellingStatus.currentPrice.value,
                'Image URL': item.galleryURL,
                'Start Time': item_start_time_uk,  # Store the UK time
            })
    # Debugging: Print how many GPT interactions occurred
    # print(gpt4o_interaction_counter)
    # print(relevant_items)
    return relevant_items


def filter_undervalued_items(items):
    """Filter items based on the condition status (e.g., GOOD CONDITION)."""
    undervalued_list = [
        item for item in items if item["Condition Status"] == "GOOD CONDITION"]
    return undervalued_list


if __name__ == "__main__":
    process_ebay_items('iPhone 12', 100, 400, 1000)
