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
        # Define the API endpoint and headers
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={st.session_state['api_key']}"
        headers = {"Content-Type": "application/json"}
        body = {
            "contents": [{"parts": [{"text": user_message}]}]
        }

        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
            data = response.json()

            # 응답에서 데이터 추출
            bot_reply = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response received.")
            st.session_state["chat_log"].append({"user": user_message, "bot": bot_reply})
        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err} (Status code: {response.status_code})")
            st.error(f"Response content: {response.text}")
        except Exception as err:
            st.error(f"An unexpected error occurred: {err}")
                
# Display chat log
st.write("### Chat Log")
for log in st.session_state["chat_log"]:
    st.write(f"**You:** {log['user']}")
    st.write(f"**Bot:** {log['bot']}")