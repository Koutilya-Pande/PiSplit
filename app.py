import streamlit as st
import pandas as pd
from data_extraction import process_image_with_ai, extract_items_and_prices
from chat_with_bill import handle_conversation

def main():
    st.title("Bill Splitting App")

    # Initialize session state variables if not already set
    if 'items_and_prices' not in st.session_state:
        st.session_state.items_and_prices = []
    if 'participant_names' not in st.session_state:
        st.session_state.participant_names = []
    if 'item_dict' not in st.session_state:
        st.session_state.item_dict = {}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Sidebar for image upload and participant names
    with st.sidebar:
        st.header("Upload Bill Image")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

        st.header("Enter Names of Participants")
        names = st.text_area("Enter the names of participants (comma-separated)")

    # Main area
    st.header("Bill Splitting and Chat")

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

        # Create a DataFrame for items and participants
        items = []
        for i, (item, price) in enumerate(st.session_state.items_and_prices):
            items.append({
                "Item": item,
                "Price": price,
                "Participants": st.multiselect(f"Who will pay for {item} (${price:.2f})?", st.session_state.participant_names, key=f"multiselect_{i}")
            })

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(items)
        
        # Display the DataFrame
        st.dataframe(df)

        # Update the session state with the selected participants
        st.session_state.item_dict = df[["Item", "Price", "Participants"]].to_dict(orient="records")

        st.header("Payment Summary")
        summary = {name: 0.0 for name in st.session_state.participant_names}

        for row in st.session_state.item_dict:
            item = row["Item"]
            price = row["Price"]
            assignees = row["Participants"]
            if assignees:
                split_price = price / len(assignees)
                for assignee in assignees:
                    summary[assignee] += split_price
            else:
                st.warning(f"No participants selected for item: {item}")

        st.write("### Amount each person owes:")
        for name, amount in summary.items():
            st.write(f"{name}: ${amount:.2f}")

        # Chat with Bill Section
        st.header("Chat with Bill")
        user_query = st.text_input("Ask about the bill:")

        if st.button("Submit"):
            if user_query:
                handle_conversation(user_query)

        # Display the entire conversation chain
        if st.session_state.chat_history:
            st.write("### Conversation:")
            for chat in st.session_state.chat_history:
                st.write(f"**You:** {chat['user']}")
                st.write(f"**AI:** {chat['ai']}")
                st.write("---")  # Separator between each interaction
    else:
        st.warning("No items and prices were extracted from the image.")

if __name__ == '__main__':
    main()
