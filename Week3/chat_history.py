# At the start of your app, after imports:
if "messages" not in st.session_state:
    st.session_state.messages = [] # Initialize if it doesn't exist

# To display existing messages:
for message in st.session_state.messages:
    # 'message' is a dictionary like {"role": "user", "content": "Hello"}
    with st.chat_message(message["role"]): # Use role for avatar (user/assistant)
        st.markdown(message["content"])   # Display content

