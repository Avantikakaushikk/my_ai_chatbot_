import streamlit as st
import asyncio
import sys
import os

# Add the backend folder to the Python path so we can import our modules directly
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))
from services.llm_service import get_response
from database import get_history, save_message

st.set_page_config(page_title="Proper AI Chatbot", page_icon="🤖", layout="wide")

st.title("🤖 AI Chatbot")
st.markdown("Welcome to the upgraded Assistant! This chatbot remembers your conversation using a SQLite database backend.")

if "user_id" not in st.session_state:
    st.session_state.user_id = "streamlit_user_1"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Directly contact the backend logic without 127.0.0.1 HTTP requests
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Typing...")
        
        try:
            # 1. Save user msg to DB
            save_message(st.session_state.user_id, "user", prompt)
            
            # 2. Fetch full history from DB
            history = get_history(st.session_state.user_id)
            
            # 3. Call LLM (Gemini) directly
            bot_reply = asyncio.run(get_response(history))
            
            # 4. Save assistant reply to DB
            save_message(st.session_state.user_id, "assistant", bot_reply)
            
            # 5. Display the response
            message_placeholder.markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            message_placeholder.markdown(f"Failed to process message: {e}")
