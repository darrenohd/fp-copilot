import streamlit as st
from dotenv import load_dotenv
from agents.document_processor import DocumentProcessor
from agents.retriever import DocumentRetriever
from agents.chat_agent import ChatAgent
from utils.vector_store import VectorStoreManager
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

st.title("Document Chat Assistant")

# Initialize components
vector_store = VectorStoreManager.initialize()
doc_processor = DocumentProcessor(vector_store)
doc_retriever = DocumentRetriever(vector_store)
chat_agent = ChatAgent()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(
        SystemMessage(content="You are an assistant for question-answering tasks.")
    )

# File upload section
uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

if uploaded_file is not None:
    with st.spinner('Processing document...'):
        if doc_processor.process_file(uploaded_file):
            st.success('Document processed successfully!')

# Display chat messages
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# Chat input
prompt = st.chat_input("Ask a question about your documents")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append(HumanMessage(content=prompt))

    context = doc_retriever.get_relevant_context(prompt)
    response = chat_agent.get_response(st.session_state.messages, context)

    with st.chat_message("assistant"):
        st.markdown(response)
        st.session_state.messages.append(AIMessage(content=response)) 