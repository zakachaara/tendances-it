import streamlit as st
import requests
import uuid

st.set_page_config(page_title="AI Customer Support", page_icon="🤖")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

st.title("🤖 AI Customer Support")
st.caption("Powered by n8n + Ollama")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("How can we help you today?"):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Send to n8n webhook
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://localhost:5678/webhook-test/customer-support",
                    json={
                        "message": prompt,
                        "user_id": st.session_state.user_id
                    },
                    timeout=500
                )
                
                if response.status_code == 200:
                    reply = response.json().get("reply", "I'm having trouble responding right now.")
                else:
                    reply = f"Error: Received status code {response.status_code}"
                
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                
            except Exception as e:
                error_msg = f"Connection error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Sidebar
with st.sidebar:
    st.header("System Info")
    st.write(f"User ID: `{st.session_state.user_id[:8]}...`")
    st.write(f"Messages: {len(st.session_state.messages)}")
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
