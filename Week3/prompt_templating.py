# Using f-strings (Python 3.6+)
user_topic = "quantum computing"
prompt = f"Explain {user_topic} in simple terms for a beginner."

# Using .format()
template = "Summarize the following text: {text_input}"
user_text = "..." # Some long text
prompt = template.format(text_input=user_text)

