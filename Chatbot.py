import os
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI

load_dotenv()

# Streamlit page setup
st.set_page_config(page_title="Simple Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Simple Chatbot")

# Initialize chat model
chat_model = AzureChatOpenAI(
   
    azure_endpoint=os.getenv("CHAT_AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("CHAT_AZURE_OPENAI_API_KEY"),
    deployment_name= os.getenv("CHAT_AZURE_OPENAI_DEPLOYMENT_NAME"),
api_version= os.getenv("CHAT_AZURE_OPENAI_API_VERSION")
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Say something..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    response = chat_model.invoke(prompt)
    answer = response.content

    # Add AI response
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
