import streamlit as st
import os
import json
from groq import Groq
from datetime import datetime

# --- Configuration --- 
DEFAULT_MODEL = "llama3-8b-8192"
EVALUATION_MODEL = "llama3-8b-8192"

# --- Helper Functions ---

def get_groq_client():
    """Initializes and returns the Groq client."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key and "groq_api_key" in st.session_state:
        api_key = st.session_state.groq_api_key
    
    if not api_key:
        st.warning("Groq API Key not found. Please enter it in the sidebar.")
        return None
    
    return Groq(api_key=api_key)

def get_current_datetime():
    """Returns the current date and time as a JSON string."""
    return json.dumps({"current_datetime": datetime.now().isoformat()})

def serialize_message(message):
    """Properly serialize message for API calls - THIS IS NECESSARY."""
    if hasattr(message, 'model_dump'):
        msg_dict = message.model_dump(exclude_unset=True)
        serialized = {
            "role": msg_dict.get("role"),
            "content": msg_dict.get("content"),
        }
        if "tool_calls" in msg_dict:
            serialized["tool_calls"] = msg_dict["tool_calls"]
        return serialized
    else:
        serialized = {
            "role": message.get("role"),
            "content": message.get("content"),
        }
        if "tool_calls" in message:
            serialized["tool_calls"] = message["tool_calls"]
        if "tool_call_id" in message:
            serialized["tool_call_id"] = message["tool_call_id"]
        if "name" in message:
            serialized["name"] = message["name"]
        return serialized

# --- Core LLM Interaction ---

def run_conversation(client, messages, model, tools=None, tool_choice="auto"):
    """Sends messages to Groq API and handles responses, including function calls."""
    system_prompt = {
        "role": "system",
        "content": """You are a specialized Coding Assistant AI with access to various tools.
        Your primary function is to help users with programming and coding-related questions.
        
        When answering coding questions, provide Python code by default unless another language is specifically requested.
        
        You have access to these tools:
        1. get_current_datetime: Get the current date and time
        
        Rules:
        1. ONLY answer questions directly related to coding, programming, algorithms, data structures, and software development
        2. Use tools when they can enhance your response
        3. When tools are used, incorporate their output naturally into your response
        4. Provide clear, concise code examples (Python by default)
        5. Reference previous conversation context when appropriate
        """
    }
    
    api_messages = [system_prompt]
    for msg in messages:
        serialized = serialize_message(msg)
        api_messages.append(serialized)
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=api_messages,
            temperature=0.7,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response.choices[0].message
    except Exception as e:
        st.error(f"Error during conversation: {e}")
        return None

def evaluate_response(client, user_query, assistant_response, model):
    """Evaluates the relevance and quality of the assistant's response."""
    eval_system_prompt = {
        "role": "system",
        "content": f"""Evaluate the assistant's response:
        User Query: "{user_query}"
        Assistant Response: "{assistant_response}"

        Criteria:
        1. **Coding Relevance:** Was the response coding-related? (Yes/No)
        2. **Helpfulness:** If relevant, how helpful? (1-5 or NA)
        3. **Refusal Appropriateness:** If irrelevant, did the assistant refuse properly? (Yes/No/NA)

        Provide evaluation starting with "Evaluation:".
        """
    }
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[eval_system_prompt],
            temperature=0.1,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Evaluation failed: {str(e)}"

# --- Streamlit App ---

st.set_page_config(page_title="Coding Assistant", layout="wide")
st.title("🧑‍💻 Groq-Powered Coding Assistant")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
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
            api_key_provided = False

    selected_model = st.selectbox(
        "Select Model",
        ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768", "gemma-7b-it"],
        index=0
    )
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.success("Chat history cleared.")
        st.rerun()

    st.markdown("---")
    st.header("🛠️ Available Tools")
    st.markdown("""
    **get_current_datetime**
    - Returns current date and time
    - Useful for time-sensitive queries
    """)
    
    st.markdown("---")
    st.markdown(
        """
        **ℹ️ About:**
        This AI assistant answers **only coding-related questions**.
        Code examples are provided in Python by default.
        """
    )
    st.caption("Built by Outskill")

# --- Initialization ---
groq_client = get_groq_client() if api_key_provided else None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Available tools
available_tools = {
    "get_current_datetime": get_current_datetime,
}

# Tools schema for the LLM
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Get the current date and time",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }
]

# --- Display Chat History ---
for idx, message in enumerate(st.session_state.messages):
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant" and message.get("content"):
        with st.chat_message("assistant"):
            st.markdown(message["content"])
            if "evaluation" in message:
                with st.expander("View Evaluation"):
                    st.info(message["evaluation"])

# --- Handle User Input ---
if prompt := st.chat_input("Ask a coding question..."):
    if not groq_client:
        st.error("Groq client not initialized. Please provide API key.")
        st.stop()

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get LLM Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response_content = ""
        assistant_message_for_state = None

        with st.spinner("🧠 Thinking..."):
            response_message = run_conversation(
                client=groq_client,
                messages=st.session_state.messages,
                model=selected_model,
                tools=tools_schema,
                tool_choice="auto",
            )

            if response_message:
                if response_message.tool_calls:
                    tool_calls_message = serialize_message(response_message)
                    st.session_state.messages.append(tool_calls_message)
                    
                    tool_results = []
                    for tool_call in response_message.tool_calls:
                        function_name = tool_call.function.name
                        tool_call_id = tool_call.id
                        
                        if function_name in available_tools:
                            with st.spinner(f"🛠️ Using: {function_name}..."):
                                try:
                                    function_response = available_tools[function_name]()
                                    
                                    tool_message = {
                                        "tool_call_id": tool_call_id,
                                        "role": "tool",
                                        "name": function_name,
                                        "content": function_response,
                                    }
                                    tool_results.append(f"[{function_name}: {function_response}]")
                                except Exception as e:
                                    tool_message = {
                                        "tool_call_id": tool_call_id,
                                        "role": "tool",
                                        "name": function_name,
                                        "content": f"Error: {str(e)}",
                                    }
                                    tool_results.append(f"[{function_name}: Error - {str(e)}]")
                                
                                st.session_state.messages.append(tool_message)
                    
                    # Show tool results
                    if tool_results:
                        with st.expander("🔧 Tool Results", expanded=True):
                            for result in tool_results:
                                st.code(result, language="json")
                    
                    # Get final response with function results
                    with st.spinner("⚙️ Processing results..."):
                        final_response = run_conversation(
                            client=groq_client,
                            messages=st.session_state.messages,
                            model=selected_model,
                            tool_choice="none",
                        )
                        
                        if final_response and final_response.content:
                            full_response_content = final_response.content
                            message_placeholder.markdown(full_response_content)
                            assistant_message_for_state = {
                                "role": "assistant",
                                "content": full_response_content
                            }
                else:
                    # Direct response
                    if response_message.content:
                        full_response_content = response_message.content
                        message_placeholder.markdown(full_response_content)
                        assistant_message_for_state = {
                            "role": "assistant",
                            "content": full_response_content
                        }

        # Evaluate response
        if full_response_content and assistant_message_for_state:
            with st.spinner("📊 Evaluating..."):
                evaluation = evaluate_response(
                    client=groq_client,
                    user_query=prompt,
                    assistant_response=full_response_content,
                    model=EVALUATION_MODEL,
                )
                assistant_message_for_state["evaluation"] = evaluation
                
                with st.expander("View Evaluation"):
                    st.info(evaluation)
            
            st.session_state.messages.append(assistant_message_for_state)

# --- Footer ---
st.markdown("---")
st.caption(f"Powered by Groq | Model: {selected_model}")