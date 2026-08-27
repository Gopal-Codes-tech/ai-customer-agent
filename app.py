import streamlit as st
import requests

st.set_page_config(page_title="Customer AI Support Agent", page_icon="🤖")
st.title("🤖 Customer Support AI Agent")
st.write("Welcome! How can I help you today?")

# Streamlit secrets se key fetch karein
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key missing! Please set GEMINI_API_KEY in .streamlit/secrets.toml")
else:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Updated REST API Endpoint (gemini-3.6-flash)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        try:
            res = requests.post(url, json=payload, headers=headers)
            if res.status_code == 200:
                data = res.json()
                bot_reply = data['candidates'][0]['content']['parts'][0]['text']
            else:
                bot_reply = f"API Error ({res.status_code}): {res.json().get('error', {}).get('message', res.text)}"
        except Exception as e:
            bot_reply = f"Error: {e}"

        with st.chat_message("assistant"):
            st.markdown(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})