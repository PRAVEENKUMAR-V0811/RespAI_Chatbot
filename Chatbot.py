from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
import os
import streamlit as st

# Store your OpenRouter API key in secrets or environment
os.environ["OPENROUTER_API_KEY"] = st.secrets["openrouter_api_key"]

llm = ChatOpenAI(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    model="deepseek/deepseek-chat-v3-0324:free",
    temperature=0.3
)

output_parser = StrOutputParser()

def get_response(history: list, user_input: str) -> str:
    messages = [("system", "You are RespAI, a helpful assistant responding clearly.")]
    for msg in history:
        messages.append((msg["role"], msg["content"]))
    messages.append(("user", user_input))

    prompt = ChatPromptTemplate.from_messages(messages)
    chain: Runnable = prompt | llm | output_parser
    return chain.invoke({})
