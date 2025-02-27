import streamlit as st
from dotenv import load_dotenv
from utils.vector_store import VectorStoreManager
from langchain_openai import ChatOpenAI
import os
import re

# Import services
from services.document_service import DocumentService
from services.scraping_service import ScrapingService

# Import tools
from tools.positioning_tool import PositioningTool
from tools.scraping_tool import ScrapingTool
from tools.slack_tool import SlackTool
from tools.rag_tool import RAGTool

# Import agent
from agents.router_agent import RouterAgent

load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="FPC | Feature Positioning Copilot",
    page_icon="🎯",
    layout="wide"
)

# Initialize tracer is now done in RouterAgent

st.title("Feature Positioning Copilot")

# Initialize services
vector_store = VectorStoreManager.initialize()
document_service = DocumentService(vector_store)
scraping_service = ScrapingService()

# Initialize tools
positioning_tool = PositioningTool(vector_store)
scraping_tool = ScrapingTool(scraping_service, document_service)
slack_tool = SlackTool()
rag_tool = RAGTool(vector_store)

# Create the agent with all tools (tracing is initialized within RouterAgent)
router_agent = RouterAgent(
    tools=[positioning_tool, scraping_tool, slack_tool, rag_tool],
    model="gpt-4"
)

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.current_analysis = None
    st.session_state.show_examples = True
    st.session_state.chat_history = []

# Add helper text in main area
st.markdown("""
### 👋 Welcome to your Feature Positioning Copilot!

Here's what you can do:
1. 📄 Upload product documents in the Context Hub (sidebar)
2. 💬 Ask questions about your product, competitors, and market
3. 🎯 Get positioning recommendations
4. 📊 Share insights to Slack
""")

# Sidebar for document upload
with st.sidebar:
    st.header("Context Hub")
    st.markdown("Upload documents to improve FPC's understanding of your product.")
    
    # Requirements upload
    with st.expander("Upload Product Requirements"):
        requirements_file = st.file_uploader("Upload PRD", type=["pdf", "txt"], key="requirements")
        if requirements_file is not None:
            if st.button("Process Requirements"):
                with st.spinner("Processing requirements document..."):
                    success = document_service.process_file(requirements_file, "requirements")
                    if success:
                        st.success("✅ Requirements processed successfully!")
                    else:
                        st.error("❌ Error processing requirements.")
    
    # User interviews upload
    with st.expander("Upload User Research"):
        interviews_file = st.file_uploader("Upload Interviews", type=["pdf", "txt"], key="interviews")
        if interviews_file is not None:
            if st.button("Process Interviews"):
                with st.spinner("Processing user interviews..."):
                    success = document_service.process_file(interviews_file, "interviews")
                    if success:
                        st.success("✅ User interviews processed successfully!")
                    else:
                        st.error("❌ Error processing interviews.")
    
    # Competitor analysis
    with st.expander("Analyze Competitor Website"):
        competitor_url = st.text_input("Competitor URL", placeholder="https://example.com/product")
        if st.button("Analyze Competitor") and competitor_url:
            with st.spinner("Analyzing competitor website..."):
                response = scraping_tool._run(competitor_url)
                st.write(response)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input at the bottom
if prompt := st.chat_input("Ask me anything about the analyzed products and documents"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = router_agent.execute(prompt, st.session_state.chat_history)
            st.markdown(response["output"])
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response["output"]})
    st.session_state.chat_history.append({"role": "assistant", "content": response["output"]}) 