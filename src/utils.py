from bs4 import BeautifulSoup  # to clean the HTML in descriptions
import re
import os
import sys
import http.client, urllib
import ssl
import certifi
from dotenv import load_dotenv

# Load environment variables (PUSH_NOTIFICATION_TOKEN, PUSH_NOTIFICATION_USER)
load_dotenv()
push_token = os.getenv('PUSH_NOTIFICATION_TOKEN')
push_user = os.getenv('PUSH_NOTIFICATION_USER')

def clean_description(description):
    """Cleans HTML from the description, removes excessive spaces and line breaks."""
    if description:
         # Parse the HTML
        soup = BeautifulSoup(description, 'html.parser')
        text = soup.get_text(separator="\n")

        # Remove multiple consecutive newlines and excessive spaces
        text = re.sub(r'\n+', '\n', text)  # Replace multiple newlines with a single newline
        text = re.sub(r'\s+', ' ', text)   # Replace multiple spaces with a single space
        text = text.strip()                # Trim leading/trailing spaces

        return text
    return "No description available."

def push_notification_sender(text):
    # print(f"Check out this {item["Title"]}, going for {item["Price"]} GBP : {item["URL"]}")
    # Use certifi's certificate bundle
    context = ssl.create_default_context(cafile=certifi.where())

    conn = http.client.HTTPSConnection("api.pushover.net:443", context=context)
    conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
            "token": push_token,
            "user": push_user,
            "message": text,
        }), { "Content-type": "application/x-www-form-urlencoded" })

    response = conn.getresponse()
    print(response.status, response.reason)