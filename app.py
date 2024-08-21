import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

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
                    st.warning(f"Failed to parse price for line: {line}")
    return items_and_prices

def main():
    st.title("Bill Splitting App")

    # Initialize session state variables if not already set
    if 'items_and_prices' not in st.session_state:
        st.session_state.items_and_prices = []
    if 'participant_names' not in st.session_state:
        st.session_state.participant_names = []
    if 'item_dict' not in st.session_state:
        st.session_state.item_dict = {}

    st.header("Upload Bill Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    st.header("Enter Names of Participants")
    names = st.text_area("Enter the names of participants (comma-separated)")

    if uploaded_file:
        image = uploaded_file.read()
        text = process_image_with_ai(image)
        st.write("Extracted Text from Image")
        st.write(text)
        
        
        st.session_state.items_and_prices = extract_items_and_prices(text)
    
    if names:
        st.session_state.participant_names = [name.strip() for name in names.split(',') if name.strip()]

    if st.session_state.items_and_prices:
        st.header("Assign Items to Participants")
        
        for i, (item, price) in enumerate(st.session_state.items_and_prices):
            st.write(f"**Item:** {item}, **Price:** ${price:.2f}")
            assigned_names = st.multiselect(
                f"Who will pay for this item?", st.session_state.participant_names, key=f"multiselect_{i}"
            )
            st.session_state.item_dict[(item, price)] = assigned_names

        st.header("Payment Summary")
        summary = {name: 0.0 for name in st.session_state.participant_names}

        for (item, price), assignees in st.session_state.item_dict.items():
            if assignees:
                split_price = price / len(assignees)
                for assignee in assignees:
                    summary[assignee] += split_price
            else:
                st.warning(f"No participants selected for item: {item}")

        st.write("### Amount each person owes:")
        for name, amount in summary.items():
            st.write(f"{name}: ${amount:.2f}")
    else:
        st.warning("No items and prices were extracted from the image.")

if __name__ == '__main__':
    main()
