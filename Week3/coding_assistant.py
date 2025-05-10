# coding_assistant_final_corrected.py
import streamlit as st
import os
import json
from groq import Groq, RateLimitError, APIError
from datetime import datetime
import time # For progress bar sleep

# --- Configuration ---
DEFAULT_MODEL = "llama3-8b-8192"
EVALUATION_MODEL = "llama3-8b-8192" # Can be the same or different

# --- Helper Functions ---

def get_groq_client():
    """Initializes and returns the Groq client."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        if "groq_api_key" in st.session_state and st.session_state.groq_api_key:
            api_key = st.session_state.groq_api_key
        else:
            st.warning(
                "Groq API Key not found. Please enter it in the sidebar or set the GROQ_API_KEY environment variable."
            )
            return None
    try:
        client = Groq(api_key=api_key)
        return client
    except APIError as e:
        st.error(f"Failed to initialize Groq client: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred during client initialization: {e}")
        return None


def get_current_datetime():
    """Returns the current date and time as a JSON string."""
    # Note: Returning JSON string as specified by OpenAI function calling standard
    return json.dumps({"current_datetime": datetime.now().isoformat()})

def filter_messages_for_api(messages):
    """Removes custom keys like 'evaluation' before sending to API."""
    api_messages = []
    for msg in messages:
        api_msg = msg.copy() # Create a copy to avoid modifying session state directly
        # Remove any keys not expected by the Groq API's chat completions endpoint
        api_msg.pop("evaluation", None)
        # Add other custom keys here if needed in the future
        api_messages.append(api_msg)
    return api_messages

# --- Core LLM Interaction ---

def run_conversation(client, messages, model, tools=None, tool_choice="auto"):
    """Sends messages to Groq API and handles responses, including function calls."""
    # System prompt defining the assistant's behavior and guardrails
    system_prompt = {
        "role": "system",
        "content": """You are a specialized Coding Assistant AI.
        Your primary function is to help users with programming and coding-related questions.
        Strictly adhere to the following rules:
        1. ONLY answer questions directly related to coding, programming languages, algorithms, data structures, software development tools, and concepts.
        2. If the user asks a question NOT related to coding, politely refuse to answer. State clearly that you can only assist with coding topics. Do not engage in off-topic conversation. Example refusal: "I specialize in coding-related questions. I cannot help with [topic of user's query]."
        3. Provide clear, concise, and accurate coding explanations or code snippets.
        4. If you need the current date or time to answer a coding-related question (e.g., about library versions released after a certain date), you can use the available 'get_current_datetime' function. Do not use it for non-coding purposes.
        5. Do not invent information. If you don't know the answer, say so.
        """,
    }
    # Prepend the system prompt to the filtered conversation history
    conversation_history = [system_prompt] + messages # messages should already be filtered

    try:
        # Pass tools and tool_choice directly as received.
        # The Groq SDK expects specific string values ("none", "auto", "required") or None for tool_choice.
        # The calling code ensures the correct value is passed based on the context (initial call vs. post-function call).
        response = client.chat.completions.create(
            model=model,
            messages=conversation_history,
            temperature=0.7,
            tools=tools, # Pass tools directly (can be None)
            tool_choice=tool_choice, # Pass tool_choice directly (should be "auto", "none", etc.)
        )
        return response.choices[0].message

    except RateLimitError:
        st.error("Rate limit reached. Please wait and try again.")
        return None
    except APIError as e:
        # Display more specific API errors if available
        st.error(f"Groq API Error: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred during conversation: {e}")
        return None

def evaluate_response(client, user_query, assistant_response, model):
    """Evaluates the relevance and quality of the assistant's response."""
    eval_system_prompt = {
        "role": "system",
        "content": f"""You are an evaluation AI. Evaluate the assistant's response based on the user's query.
        User Query: "{user_query}"
        Assistant Response: "{assistant_response}"

        Evaluate based on these criteria:
        1.  **Coding Relevance:** Was the assistant's response strictly related to coding/programming topics? (Yes/No)
        2.  **Helpfulness (if relevant):** If the response was coding-related, how helpful and accurate was it? (Score 1-5, 5=Excellent, 1=Not Helpful, NA if not relevant)
        3.  **Refusal Appropriateness (if irrelevant):** If the user's query was *not* coding-related, did the assistant politely refuse according to its instructions? (Yes/No/NA)

        Provide the evaluation concisely, starting with "Evaluation:".
        Example (Relevant): "Evaluation: Coding Relevance: Yes, Helpfulness: 4/5, Refusal Appropriateness: NA"
        Example (Irrelevant, Correct Refusal): "Evaluation: Coding Relevance: No, Helpfulness: NA, Refusal Appropriateness: Yes"
        Example (Irrelevant, Failed Refusal): "Evaluation: Coding Relevance: No, Helpfulness: NA, Refusal Appropriateness: No"
        """,
    }
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[eval_system_prompt],
            temperature=0.1, # Low temperature for consistent evaluation
        )
        return response.choices[0].message.content
    except RateLimitError:
        st.warning("Evaluation failed due to rate limit.")
        return "Evaluation failed (Rate Limit)."
    except APIError as e:
        st.warning(f"Could not evaluate the response due to API error: {e}")
        return f"Evaluation failed (API Error: {e})."
    except Exception as e:
        st.warning(f"Could not evaluate the response: {e}")
        return f"Evaluation failed ({type(e).__name__})."


# --- Streamlit App ---

st.set_page_config(page_title="Coding Assistant", layout="wide")
st.title("🧑‍💻 Groq-Powered Coding Assistant")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configuration")
    # Handle API Key Input
    api_key_provided = False
    if "GROQ_API_KEY" in os.environ:
        st.success("Groq API Key found in environment variables.")
        api_key_provided = True
    else:
        groq_api_key_input = st.text_input(
            "Groq API Key", type="password", key="api_key_input",
            help="Get your key from https://console.groq.com/keys"
        )
        if groq_api_key_input:
            st.session_state.groq_api_key = groq_api_key_input
            api_key_provided = True
        else:
            st.warning("Please enter your Groq API Key.")

    selected_model = st.selectbox(
        "Select Model",
        ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768", "gemma-7b-it"],
        index=0 # Default to llama3-8b
    )
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.success("Chat history cleared.")
        st.rerun() # Rerun to reflect the cleared history immediately

    st.markdown("---")
    st.markdown(
        """
        **ℹ️ About:**
        This AI assistant is designed to answer **only coding-related questions**.
        It uses Llama3 (or other selected models) via the Groq API for fast responses.

        **✨ Features:**
        - System Prompts & Guardrails
        - Chat Memory
        - Function Calling (for current time)
        - Response Evaluation
        - Streamlit UI Elements
        """
    )
    st.markdown("---")
    st.caption("Built by T3 Chat") # Or your name/team

# --- Initialization ---
groq_client = get_groq_client() if api_key_provided else None

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Define available tools for the LLM
available_tools = {
    "get_current_datetime": get_current_datetime,
}

# Define the schema for the tools that the LLM can use
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Get the current date and time as an ISO formatted string in JSON. Useful for time-sensitive coding questions (e.g., library release dates, checking against current time). Only use if specifically needed for a coding context.",
            "parameters": { # Define parameters even if empty
                 "type": "object",
                 "properties": {},
                 "required": [],
            },
        },
    }
]


# --- Display Chat History ---
# Iterate through the messages stored in session state
for message in st.session_state.messages:
    # Display user messages
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    # Display assistant messages (checking for content to avoid errors)
    elif message["role"] == "assistant" and message.get("content"):
         with st.chat_message("assistant"):
            st.markdown(message["content"])
            # Display evaluation if it exists for this message, inside an expander
            if "evaluation" in message:
                with st.expander("View Evaluation"):
                    st.info(message["evaluation"])
    # Note: We don't display 'system', 'tool', or 'assistant' messages
    # that only contain tool_calls without content.

# --- Handle User Input ---
if prompt := st.chat_input("Ask a coding question..."):
    if not groq_client:
        st.error("Groq client not initialized. Please provide API key in the sidebar.")
        st.stop() # Stop execution if client isn't ready

    # Add user message to app history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Get LLM Response (potentially with function calling) ---
    with st.chat_message("assistant"):
        message_placeholder = st.empty() # For streaming-like effect or final display
        full_response_content = ""
        assistant_final_msg_for_state = {} # Store the message to be added to state

        with st.spinner("🧠 Thinking..."):
            # Filter messages to remove custom keys before sending to API
            messages_for_api_call = filter_messages_for_api(st.session_state.messages)

            # Initial call to the LLM
            response_message = run_conversation(
                client=groq_client,
                messages=messages_for_api_call, # Use filtered messages
                model=selected_model,
                tools=tools_schema,
                tool_choice="auto", # Let the model decide if it needs a tool
            )

            if response_message:
                # Check if the LLM response includes a request to call a tool
                if response_message.tool_calls:
                    # Function call requested by the LLM
                    # Add the assistant's response containing the tool_calls request to history
                    # We use model_dump to get a serializable dictionary
                    st.session_state.messages.append(response_message.model_dump(exclude_unset=True))

                    tool_results_messages = [] # Store results of tool calls

                    # Process each tool call requested
                    for tool_call in response_message.tool_calls:
                        function_name = tool_call.function.name
                        tool_call_id = tool_call.id

                        if function_name in available_tools:
                            function_to_call = available_tools[function_name]
                            try:
                                # Arguments are in tool_call.function.arguments (JSON string)
                                # For get_current_datetime, arguments are empty/ignored
                                # function_args = json.loads(tool_call.function.arguments) # Use if args needed
                                with st.spinner(f"🛠️ Calling function: `{function_name}`..."):
                                    function_response = function_to_call() # Call the function

                                # Add function response to history for the next LLM call
                                tool_results_messages.append(
                                    {
                                        "tool_call_id": tool_call_id,
                                        "role": "tool",
                                        "name": function_name,
                                        "content": function_response, # Must be a string
                                    }
                                )
                            except Exception as e:
                                st.error(f"Error executing function {function_name}: {e}")
                                tool_results_messages.append(
                                     {
                                        "tool_call_id": tool_call_id,
                                        "role": "tool",
                                        "name": function_name,
                                        "content": f"Error executing function: {e}",
                                    }
                                )
                        else:
                             st.error(f"Function '{function_name}' not found.")
                             tool_results_messages.append(
                                {
                                    "tool_call_id": tool_call_id,
                                    "role": "tool",
                                    "name": function_name,
                                    "content": f"Error: Function '{function_name}' is not defined.",
                                }
                            )

                    # Add all tool results to the main session state history
                    st.session_state.messages.extend(tool_results_messages)

                    # Second call to LLM with function results included in history
                    with st.spinner("⚙️ Processing function results..."):
                         # Filter messages again, now including the tool request and results
                         messages_for_api_call_2 = filter_messages_for_api(st.session_state.messages)
                         final_response_message = run_conversation(
                            client=groq_client,
                            messages=messages_for_api_call_2, # Use updated filtered list
                            model=selected_model,
                            tool_choice="none", # Explicitly tell the model not to call functions again
                        )
                         if final_response_message and final_response_message.content:
                             full_response_content = final_response_message.content
                             message_placeholder.markdown(full_response_content)
                             # Prepare the final message object for session state
                             assistant_final_msg_for_state = final_response_message.model_dump(exclude_unset=True)
                         else:
                             error_msg = "Sorry, I encountered an error after processing the function call."
                             full_response_content = error_msg
                             message_placeholder.error(error_msg)
                             assistant_final_msg_for_state = {"role": "assistant", "content": error_msg}

                else:
                    # No function call, direct response from the first call
                    if response_message.content:
                        full_response_content = response_message.content
                        message_placeholder.markdown(full_response_content)
                        # Prepare the final message object for session state
                        assistant_final_msg_for_state = response_message.model_dump(exclude_unset=True)
                    else:
                        # Handle cases where the response might be empty or only have tool_calls (though handled above)
                        error_msg = "Sorry, I received an unexpected empty response."
                        full_response_content = error_msg
                        message_placeholder.warning(error_msg) # Use warning for potentially non-critical empty response
                        assistant_final_msg_for_state = {"role": "assistant", "content": error_msg}

            else:
                # Handle case where the initial run_conversation returned None (due to API error, etc.)
                error_msg = "Sorry, I couldn't get a response due to an error."
                full_response_content = error_msg # Set for evaluation purposes
                message_placeholder.error(error_msg)
                assistant_final_msg_for_state = {"role": "assistant", "content": error_msg}


        # --- Evaluate the final response ---
        # Ensure there's content to evaluate and it's not just an error message placeholder
        if full_response_content and assistant_final_msg_for_state.get("role") == "assistant":
             with st.spinner("📊 Evaluating response..."):
                evaluation_result = evaluate_response(
                    client=groq_client,
                    user_query=prompt,
                    assistant_response=full_response_content,
                    model=EVALUATION_MODEL, # Use the designated evaluation model
                )
                # Add evaluation result to the message dictionary destined for session state
                # This is safe because it happens *before* adding to state, and filtering
                # occurs *before* the next API call.
                assistant_final_msg_for_state["evaluation"] = evaluation_result
                # Display evaluation immediately in an expander below the response
                with st.expander("View Evaluation"):
                    st.info(evaluation_result)
        else:
             # If there was no valid content (e.g., error occurred before response generation)
             assistant_final_msg_for_state["evaluation"] = "Evaluation skipped (no valid response content)."
             with st.expander("View Evaluation"):
                 st.warning("Evaluation skipped (no valid response content).")


        # Add the final assistant message (with content and evaluation) to session state
        # Check if the message object is not empty before appending
        if assistant_final_msg_for_state:
            st.session_state.messages.append(assistant_final_msg_for_state)

        # Add a small progress bar effect at the end (optional aesthetic)
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.005) # Very short sleep
            progress_bar.progress(percent_complete + 1)
        progress_bar.empty() # Remove progress bar

# --- Footer ---
st.markdown("---")
st.caption(f"Powered by Groq | Model: {selected_model}")
