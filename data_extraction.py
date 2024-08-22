# data_extraction.py

import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def process_image_with_ai(image):
    """Use an AI model to extract items and prices from the image."""
    image_data = {
        "mime_type": "image/jpeg",  # or the appropriate mime type for your image
        "data": image
    }
    prompt = """
    You are an expert in extracting structured data from images.
    You will be provided with an image of a bill. Extract the items and their corresponding prices and return the result as the below format.
    For example:
    Item 1  12.50
    Item 2  8.99
    Item 3  15.00
    """
    
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([image_data, prompt])
    return response.text

def extract_items_and_prices(text):
    """Extract items and prices from the text using regular expressions."""
    items_and_prices = []
    pattern = r'(.*?)(\d+(\.\d{2})?)$'
    
    for line in text.splitlines():
        line = line.strip()
        if line:
            match = re.search(pattern, line)
            if match:
                item_name = match.group(1).strip()
                item_price = match.group(2).strip()
                try:
                    item_price = float(item_price)
                    items_and_prices.append((item_name, item_price))
                except ValueError:
                    print(f"Failed to parse price for line: {line}")
    return items_and_prices
