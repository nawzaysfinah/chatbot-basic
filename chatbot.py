import streamlit as st
import google.generativeai as genai
import os

# Get API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY environment variable is not set. Please set it and restart the application.")
    st.stop()

# Set up Gemini API
genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-pro')

# Streamlit app
st.title("Gemini 1.5 Flash Chatbot")

# Add descriptive text
st.markdown("This is a test of the Gemini 1.5 Flash API. Code is generated exclusively using Claude 3.5 Sonnet")

# Add a separator
st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get Gemini's response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            chat = model.start_chat(history=[
                {"role": m["role"], "parts": [m["content"]]}
                for m in st.session_state.messages
            ])
            response = chat.send_message(prompt, stream=True)
            
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Add Gemini's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Clear chat history button
if st.button("Clear Chat History"):
    st.session_state.messages = []