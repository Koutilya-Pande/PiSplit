# chat_with_bill.py

import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables (assuming you're using a .env file)
load_dotenv()

# Configure Google Gemini AI with API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def handle_conversation(user_query):
    """Handles the conversation with the AI about the bill."""
    if not st.session_state.items_and_prices:
        st.write("No bill data available to chat about.")
        return
    
    # Use the AI model to respond to the user query
    response = generate_ai_response(user_query)
    
    # Update chat history
    st.session_state.chat_history.append({"user": user_query, "ai": response})

def generate_ai_response(user_query):
    """Generates a conversational response from AI based on user query."""
    # Create a custom prompt for the AI
    items_and_prices_text = "\n".join([f"{item}: ${price:.2f}" for item, price in st.session_state.items_and_prices])
    prompt = f"""
    You are an expert on understanding bills. Here is a list of items and prices extracted from a bill:
    
    {items_and_prices_text}
    
    A user will now ask you questions related to the bill. Please respond based on the items, prices, and any relevant details. Be as helpful as possible.

    User's question: "{user_query}"
    """
    
    # Example AI call (replace with actual API call to Google Gemini, OpenAI, etc.)
    response = generate_response_from_ai(prompt)
    return response

def generate_response_from_ai(prompt):
    """Generates a response from Google Gemini AI model based on the prompt."""
    try:
        # Generate the response using the Gemini API
        model = genai.GenerativeModel("gemini-1.5-flash")  # Use the appropriate Gemini model
        response = model.generate_content(prompt)
        return response.text
        

    
    except Exception as e:
        # Handle any errors during the API call
        return f"An error occurred while generating the response: {str(e)}"
