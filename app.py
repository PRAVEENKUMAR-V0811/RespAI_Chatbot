from datetime import datetime
import streamlit as st
from Chatbot import get_response
from openai import RateLimitError
import traceback

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
- Built using LangChain and Streamlit
                    
_RespAI: Responding to your thoughts, intelligently._
""")
st.sidebar.info("⚠️ _Note: At peak times, you may experience short delays due to server load. Thanks for your patience._")

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
            try:
                response = get_response(st.session_state.messages, prompt)
                st.markdown(response)
            except RateLimitError:
                st.warning("⚠️ We're currently experiencing high demand. Please wait a few seconds and try again.")
                response = "Sorry, I’m temporarily unavailable due to high traffic. Please try again shortly."
            except Exception as e:
                st.error("⚠️ An unexpected error occurred. Please try again later.")
                st.write("**Debug info:**", str(e))  # Show error message
                st.code(traceback.format_exc())       # Show full traceback in UI
                response = "An error occurred while processing your request."
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
