import streamlit as st
import os
# We'll add 'from groq import Groq, APIError' soon

# Configure the page title and layout
st.set_page_config(page_title="Coding Assistant", layout="wide")

# Display the main title of the application
st.title("🧑‍💻 Groq-Powered Coding Assistant")

# Create a sidebar for configuration options
with st.sidebar:
    st.header("⚙️ Configuration")
    # API key input will go here

