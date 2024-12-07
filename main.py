from streamlit_chat import message
import streamlit as st
import requests

API_KEY = "your_API"
API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Streamlit app with 
st.title("الفضاء")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for i, msg in enumerate(st.session_state.messages):  # Use enumerate for unique keys
    message(msg["content"], is_user=(msg["role"] == "user"), key=f"message_{i}")

if user_input := st.chat_input("وش تبي تعرف عن الفضاء ؟"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    message(user_input, is_user=True, key=f"user_input_{len(st.session_state.messages)}")

    prompt = f"بصفتك عالم فضاء، أجب على الأسئلة  باللغه العربيه فقط: {user_input}"

    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100,
        "temperature": 0.6
        # "temperature": 0.6
        # "temperature": 0.7

    }
    #API key 
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        bot_response = data['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "bot", "content": bot_response})
        message(bot_response, key=f"bot_response_{len(st.session_state.messages)}")
    else:
        error_message = f"Error: {response.status_code}, {response.text}"
        st.session_state.messages.append({"role": "bot", "content": error_message})
        message(error_message, key=f"error_response_{len(st.session_state.messages)}")
