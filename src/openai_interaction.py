import os
from openai import OpenAI
from openai import OpenAIError
from dotenv import load_dotenv

# Loading API key from the .env file
load_dotenv()
api_key = os.environ['OPENAI_API_KEY']

# Check if the API key is loaded, raise an error if not
if not api_key:
    raise ValueError("API key not found. Check the OPENAI_API_KEY in the .env file.")

# Initialize the OpenAI client with the provided API key
client = OpenAI(api_key=api_key)

def get_openai_response(prompt, model="gpt-4o"):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role":"user",
                    "content":prompt,
                }
            ],
            model=model
        )
        return response.choices[0].message.content.strip()
    except OpenAIError as e:
         print(f"An error occured: {e}")
         return None


def analyze_item_condition(description, item_title):
    # Create the prompt with the item's description
    item_status_prompt = f"You have condition to check. Analyze the provided description. If the description mentions any vulnerabilities (e.g., broken screen, cracked glass, non-functional components, faulty charging port, bad battery condition - less than 85% of battery condition), return 'BAD CONDITION'. If no such issues are mentioned, return 'GOOD CONDITION'. If there is no description whatsoever, return 'GOOD CONDITION' UNDER ANY CIRTUMSTANCES DON'T WRITE OTHER WORDS THAN 'GOOD CONDITION' OR 'BAD CONDITION'. Description: {description}"




    # Send the prompt to GPT API (you'd have your OpenAI API integration here)
    response = get_openai_response(item_status_prompt)  # Placeholder function for API call
    return response.strip()  # response is a simple GOOD CONDITION/BAD CONDITION
