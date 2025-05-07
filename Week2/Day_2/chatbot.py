import streamlit as st
import requests
import os

# Set page configuration
st.set_page_config(page_title="Chatbot Interface", layout="wide")

# App title
st.title("Hugging Face Chatbot")

# Initialize session state variables if they don't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

if "hf_key" not in st.session_state:
    st.session_state.hf_key = ""

# Sidebar for API key input
with st.sidebar:
    st.header("Configuration")
    hf_key = st.text_input("Enter your HuggingFace API key:", type="password")
    if hf_key:
        st.session_state.hf_key = hf_key

    # Button to start a new conversation
    if st.button("New Conversation"):
        st.session_state.messages = []
        st.rerun()

# Configure API details
API_URL = "https://router.huggingface.co/together/v1/chat/completions"

def query(payload, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: API returned status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Request Error: {e}")
        return None

# Display the conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask something..."):
    if not st.session_state.hf_key:
        st.error("Please enter your HuggingFace API key in the sidebar.")
    else:
        # Add user message to the chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display the user message
        with st.chat_message("user"):
            st.write(prompt)

        # Display a spinner while waiting for the API response
        with st.spinner("Thinking..."):
            # Prepare the payload with only the current query (no history)
            payload = {
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 512,
                "model": "mistralai/Mistral-7B-Instruct-v0.3"
            }

            # Query the API
            response = query(payload, st.session_state.hf_key)

            if response and "choices" in response and len(response["choices"]) > 0:
                bot_response = response["choices"][0]["message"]["content"]

                # Add assistant response to the chat history
                st.session_state.messages.append({"role": "assistant", "content": bot_response})

                # Display the assistant response
                with st.chat_message("assistant"):
                    st.write(bot_response)
            else:
                st.error("Failed to get a valid response from the API.")

# Display information and instructions
with st.expander("How to use this chatbot"):
    st.write("""
    1. Enter your HuggingFace API key in the sidebar.
    2. Type your question in the input box at the bottom of the page.
    3. View the response and continue the conversation.
    4. Click 'New Conversation' in the sidebar to start fresh.
    """)