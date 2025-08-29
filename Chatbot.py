import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType

load_dotenv()

# Streamlit setup
st.set_page_config(page_title="Simple Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Simple Chatbot with DuckDuckGo")

# Initialize model
chat_model = AzureChatOpenAI(
    azure_endpoint=os.getenv("CHAT_AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("CHAT_AZURE_OPENAI_API_KEY"),
    deployment_name=os.getenv("CHAT_AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_version=os.getenv("CHAT_AZURE_OPENAI_API_VERSION")
)

# Add DuckDuckGo search tool
search = DuckDuckGoSearchRun()

# Initialize agent with search ability
agent = initialize_agent(
    tools=[search],
    llm=chat_model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Use agent (model + DuckDuckGo)
    answer = agent.run(prompt)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
