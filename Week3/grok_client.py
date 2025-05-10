from groq import Groq, APIError # Add this import at the top

def get_groq_client():
    """Initializes and returns the Groq client."""
    # Try to get API key from environment variable first
    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key: # If not in environment, check session_state (from user input)
        if "groq_api_key" in st.session_state and st.session_state.groq_api_key:
            api_key = st.session_state.groq_api_key
        else:
            st.warning(
                "Groq API Key not found. Please enter it in the sidebar."
            )
            return None # No key, no client
    try:
        client = Groq(api_key=api_key)
        return client
    except APIError as e: # Specific error from Groq SDK
        st.error(f"Failed to initialize Groq client (APIError): {e}")
        return None
    except Exception as e: # Other potential errors
        st.error(f"An unexpected error occurred during client initialization: {e}")
        return None

# In the sidebar:
# api_key_input = st.text_input("Groq API Key", type="password", key="api_key_input")
# if api_key_input: st.session_state.groq_api_key = api_key_input

# In main app flow, after sidebar:
# groq_client = get_groq_client()

