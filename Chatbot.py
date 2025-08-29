import os
import streamlit as st
import requests
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()

# Streamlit page setup
st.set_page_config(page_title="Simple Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Simple Chatbot Using Streamlit (with Latest News)")

# Initialize chat model
chat_model = AzureChatOpenAI(
    azure_endpoint=os.getenv("CHAT_AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("CHAT_AZURE_OPENAI_API_KEY"),
    deployment_name=os.getenv("CHAT_AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_version=os.getenv("CHAT_AZURE_OPENAI_API_VERSION")
)

# Function to fetch latest news/data from DuckDuckGo
def get_latest_news(query: str) -> str:
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    try:
        res = requests.get(url, timeout=10).json()
        abstract = res.get("AbstractText")
        related_topics = res.get("RelatedTopics", [])
        if abstract:
            return abstract
        elif related_topics:
            return related_topics[0].get("Text", "No detailed news found.")
        else:
            return "No news found."
    except Exception as e:
        return f"Error fetching news: {e}"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me something..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check if user wants latest news/data
    if any(word in prompt.lower() for word in ["latest", "news", "today", "current", "update"]):
        fetched_news = get_latest_news(prompt)
        response = chat_model.invoke(
            f"User asked: {prompt}\nHere is the latest information I found online: {fetched_news}\n"
            f"Please summarize and answer naturally."
        )
    else:
        # Normal LLM response
        response = chat_model.invoke(prompt)

    answer = response.content

    # Add AI response
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
