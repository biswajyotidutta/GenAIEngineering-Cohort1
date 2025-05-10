# Chatbot Implementation Homework

## Current Implementation Shortcoming

The current chatbot implementation has a significant limitation: **it does not maintain conversational context between messages**. While the conversation history is displayed in the user interface, each query to the API is sent independently without any reference to previous exchanges.

This creates several problems:

1. The chatbot cannot reference information from previous messages
2. Users must repeat context in each new question
3. Multi-turn conversations requiring follow-up questions don't work naturally
4. The chatbot appears to "forget" what was just discussed

## Your Assignment

### 1. Modify the API Request to Include Conversation History

Update the solution to respond with context of previous questions

### Food for thought

1. Service that responds to queries from UI such that Streamlit does not use LLM, Streamlit only take input and requests a service
2. Persist conversations and retrieve as needed
3. organize data and real-estate
4. Tools as plug-ins

Good luck!
