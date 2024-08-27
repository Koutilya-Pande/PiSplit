import streamlit as st
import google.generativeai as genai

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
    You are assisting in managing a bill splitting scenario. You will be given the bill, items and price will be listed on this. The items might not have their full name but you can predict what item it is like CHCLATE is CHOCOLATE like this. You can use this technique to answer more accurately.  
    Here is the current bill:
    {st.session_state.items_and_prices}
    
    The participants are: {st.session_state.participant_names}
    
    User Query: {user_query}

    You will be asked questions like what product got splitted in whom? or whats the price of the product? Prepare yourself accordingly, and help upto your best quality.  
    Respond with the necessary updates, assignments, or corrections that need to be made to the bill splitting process based on the user query.
    """

    # Example AI call (replace with actual API call to Google Gemini, OpenAI, etc.)
    response = generate_response_from_ai(prompt)
    return response

def generate_response_from_ai(prompt):
    """Generates a response from Google Gemini AI model based on the prompt."""
    try:
        # Check if the API key is available
        api_key = st.session_state.api_key
        if not api_key:
            raise ValueError("API key is not set.")
        
        # Configure the AI model with the user-provided API key
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")  # Use the appropriate Gemini model
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Handle any errors during the API call
        return f"An error occurred while generating the response: {str(e)}"
