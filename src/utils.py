from bs4 import BeautifulSoup  # to clean the HTML in descriptions
import re

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