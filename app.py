import streamlit as st
import requests

# Sidebar for Gemini API Key input
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")
if st.sidebar.button("Save API Key"):
    if api_key:
        st.session_state["api_key"] = api_key
        st.sidebar.success("API Key saved!")
    else:
        st.sidebar.error("API Key cannot be empty.")

# Chat Interface
st.title("Gemini ChatBot")

# Initialize session state for chat log
if "chat_log" not in st.session_state:
    st.session_state["chat_log"] = []

# User input
user_message = st.text_input("Type your message here:", "")
if st.button("Send"):
    if "api_key" not in st.session_state or not st.session_state["api_key"]:
        st.error("Please enter your Gemini API key in the sidebar.")
    elif user_message:
        # Send message to Gemini API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={st.session_state['api_key']}"
        headers = {"Content-Type": "application/json"}
        body = {
            "contents": [{"parts": [{"text": user_message}]}]
        }

        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            data = response.json()
            bot_reply = data.get("contents", [{}])[0].get("parts", [{}])[0].get("text", "No response received.")
            # Update chat log
            st.session_state["chat_log"].append({"user": user_message, "bot": bot_reply})
        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with Gemini API: {e}")

# Display chat log
st.write("### Chat Log")
for log in st.session_state["chat_log"]:
    st.write(f"**You:** {log['user']}")
    st.write(f"**Bot:** {log['bot']}")