import streamlit as st
from dotenv import load_dotenv
from agents.document_processor import DocumentProcessor
from agents.product_positioning import ProductPositioningAgent
from agents.tools_manager import PositioningTools
from utils.vector_store import VectorStoreManager
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from agents.web_scraper import WebScraper

load_dotenv()

st.title("Product Positioning Assistant")

# Initialize components
vector_store = VectorStoreManager.initialize()
doc_processor = DocumentProcessor(vector_store)
positioning_agent = ProductPositioningAgent(vector_store)
tools_manager = PositioningTools(positioning_agent)

# File upload section
with st.sidebar:
    st.header("Document Sources")
    st.write("Upload documents to analyze for positioning insights:")
    
    uploaded_files = st.file_uploader(
        "Upload Documents", 
        type=["pdf", "csv", "txt"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for doc in uploaded_files:
            with st.spinner(f'Processing {doc.name}...'):
                doc_processor.process_file(doc)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    initial_message = """I'm your product positioning assistant. I can help you analyze your product positioning using these tools:
    
    {}
    
    How can I help you today?""".format(tools_manager.get_tool_descriptions())
    
    st.session_state.messages.append(SystemMessage(content=initial_message))

# Display chat messages
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)
    elif isinstance(message, SystemMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# Chat input
prompt = st.chat_input("How can I help you with product positioning?")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append(HumanMessage(content=prompt))
    
    # Process the command and execute appropriate tool
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            # Here you would add logic to parse the prompt and determine which tool to use
            # For now, we'll use a simple string matching approach
            if "market fit" in prompt.lower():
                result = tools_manager.execute_tool("analyze_market_fit")
            elif "value prop" in prompt.lower():
                result = tools_manager.execute_tool("extract_value_props")
            elif "competitive" in prompt.lower():
                st.text_input_container = st.empty()
                competitor_url = st.text_input("Please provide the competitor's website URL:")
                
                if competitor_url:
                    with st.spinner("Analyzing competitor website..."):
                        # Initialize web scraper
                        scraper = WebScraper()
                        competitor_data = scraper.scrape_website(competitor_url)
                        
                        # Add to vector store for analysis
                        doc_processor.process_text(
                            text=competitor_data['main_content'],
                            metadata={'source': competitor_url}
                        )
                        
                        # Run competitive analysis
                        result = tools_manager.execute_tool(
                            "analyze_competitive_position",
                            competitor_url=competitor_url
                        )
                else:
                    result = "Please provide a competitor's website URL to analyze."
            elif "positioning statement" in prompt.lower():
                # Extract parameters from prompt or ask for them
                result = "Please provide target segment and key benefits for generating a positioning statement."
            else:
                result = f"I can help you with the following tools:\n{tools_manager.get_tool_descriptions()}"
            
            st.markdown(result)
            st.session_state.messages.append(AIMessage(content=result)) 