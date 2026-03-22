import streamlit as st
import requests

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

    # Send request to backend
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Typing...")
        
        try:
            response = requests.post("http://127.0.0.1:8000/chat/", json={
                "user_id": st.session_state.user_id,
                "message": prompt
            })
            if response.status_code == 200:
                bot_reply = response.json().get("response", "Error getting response.")
                message_placeholder.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            else:
                message_placeholder.markdown(f"API Error: {response.status_code}")
        except Exception as e:
            message_placeholder.markdown(f"Failed to connect to backend: {e}")
