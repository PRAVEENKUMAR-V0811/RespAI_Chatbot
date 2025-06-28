from datetime import datetime
import streamlit as st
from Chatbot import get_response
from fpdf import FPDF

st.set_page_config(
    page_title="RespAI",
    page_icon="favicon.ico",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- SIDEBAR ---
st.sidebar.title("⚙️ Chat Settings")

# New Chat
if st.sidebar.button("➕ Start New Chat"):
    st.session_state.messages = []
    st.sidebar.success("Started a new conversation.")
    st.rerun()


# Bot Info (Footer)
st.sidebar.markdown("---")
st.sidebar.markdown("### About RespAI")
st.sidebar.markdown("""
**RespAI** is a context-aware conversational assistant built with DeepSeek via OpenRouter.

- Delivers accurate, structured responses  
- Maintains session-based context  
- Built using LangChain and Streamlit
                    
_RespAI: Responding to your thoughts, intelligently._
""")

st.title("RespAI")

now = datetime.now()
hour = now.hour
if hour < 12:
    greeting = "Good Morning"
elif hour < 14:
    greeting = "Good Afternoon"
else:
    greeting = "Good Evening"

with st.chat_message("assistant"):
    st.write(f" {greeting} ! - Welcome to RespAI!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Say what's on your mind !"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
   
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_response(st.session_state.messages, prompt)
            st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})