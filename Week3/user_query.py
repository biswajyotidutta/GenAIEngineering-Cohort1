# Place this after displaying chat history
if prompt := st.chat_input("Ask a coding question..."): # Gets user input
    if not groq_client: # Make sure client is ready
        st.error("Groq client not initialized. Please provide API key.")
        st.stop() # Halt further execution if no client

    # 1. Add user's message to our history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Display user's message immediately in the chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Now, get the assistant's response (covered next)
    # ... assistant_response = get_llm_reply(prompt) ...

