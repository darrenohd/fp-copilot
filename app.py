import streamlit as st
from dotenv import load_dotenv
from agents.document_processor import DocumentProcessor
from utils.vector_store import VectorStoreManager
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from agents.positioning_agent import PositioningAgent
from agents.scraping_agent import ScrapingAgent
from agents.slack_agent import SlackAgent
from utils.tracing import initialize_tracer
from agents.prompts.routing import AGENT_ROUTING_PROMPT
import re
import os

load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="FPC | Feature Positioning Copilot",
    page_icon="🎯",
    layout="wide"
)

# Initialize tracer
tracer_provider = initialize_tracer()

st.title("Feature Positioning Copilot")

# Initialize components
vector_store = VectorStoreManager.initialize()
document_processor = DocumentProcessor(vector_store)

# Initialize agents
positioning_agent = PositioningAgent(vector_store)
scraping_agent = ScrapingAgent(vector_store)
slack_agent = SlackAgent()  # Create the SlackAgent

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.current_analysis = None
    st.session_state.show_examples = True

# Add helper text in main area
st.markdown("""
### 👋 Welcome to your Feature Positioning Copilot!

Here's what you can do:
1. 📄 Upload product documents in the Context Hub (sidebar)
2. 💬 Ask questions about your product, competitors, and market
3. 🎯 Get positioning recommendations
4. 📊 Share insights to Slack
""")

# Sidebar for document uploads
with st.sidebar:
    st.header("📚 Context Hub")
    
    # Feature Information Section
    with st.expander("Feature Information", expanded=True):
        st.subheader("Basic Details")
        feature_name = st.text_input("Feature Name", key="feature_name")
        release_date = st.date_input("Target Release Date", key="release_date")
        
        if all([feature_name, release_date]):
            st.session_state.feature_info = {
                "name": feature_name,
                "release_date": release_date
            }
    
    # Requirements Section
    with st.expander("Requirements", expanded=False):
        st.subheader("Product Requirements")
        requirements_file = st.file_uploader("Upload Product Requirements", type=['txt', 'pdf'], key="req_upload")
        if requirements_file and st.button("Process Requirements", key="req_button"):
            with st.spinner("Processing requirements document..."):
                document_processor.process_file(requirements_file, "requirements")
                st.success("Requirements processed!")
    
    # User Interviews Section
    with st.expander("User Research", expanded=False):
        st.subheader("User Interviews")
        interviews_file = st.file_uploader("Upload User Interviews", type=['txt', 'pdf'], key="int_upload")
        if interviews_file and st.button("Process Interviews", key="int_button"):
            with st.spinner("Processing interviews..."):
                document_processor.process_file(interviews_file, "interviews")
                st.success("Interviews processed!")
    
    # Competitor Analysis Section
    with st.expander("Competitor Analysis", expanded=False):
        st.subheader("Competitor URLs")
        competitor_url = st.text_input("Enter competitor URL")
        if competitor_url and st.button("Analyze Competitor", key="comp_button"):
            with st.spinner("Analyzing competitor..."):
                analysis = scraping_agent.execute(competitor_url)
                if isinstance(analysis, str):
                    st.error(analysis)
                else:
                    document_processor.process_competitor(analysis)
                    st.success("Competitor analyzed and stored!")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Only show example buttons if no messages yet
if st.session_state.show_examples and len(st.session_state.messages) == 0:
    st.write("Try these example questions:")
    container = st.container()
    with container:
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
        with col1:
            if st.button("Generate a positioning statement", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Generate a positioning statement for our product"})
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        positioning = positioning_agent.execute()
                        st.markdown(positioning)
                st.session_state.messages.append({"role": "assistant", "content": positioning})
                st.session_state.show_examples = False
                st.rerun()

# Chat input at the bottom
if prompt := st.chat_input("Ask me anything about the analyzed products and documents"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Determine which agent to use
            routing_prompt = AGENT_ROUTING_PROMPT.format(user_request=prompt)
            router = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            agent_to_use = router.invoke(routing_prompt).content.strip()
            
            # Route to appropriate agent
            if agent_to_use == "SlackAgent" or "share to slack" in prompt.lower():
                if len(st.session_state.messages) > 1:
                    last_message = st.session_state.messages[-2]["content"]
                    success, message = slack_agent.execute(last_message)
                    response = "✅ " + message if success else "❌ " + message
                else:
                    response = "❌ No previous message to share!"
            elif agent_to_use == "PositioningAgent":
                positioning = positioning_agent.execute()
                response = positioning
            elif agent_to_use == "ScrapingAgent":
                # Extract URL from prompt
                url_match = re.search(r'https?://[^\s]+', prompt)
                if url_match:
                    url = url_match.group(0)
                    product_data = scraping_agent.execute(url)
                    if product_data:
                        response = f"✅ Successfully analyzed {url}. Here's what I found:\n\n"
                        response += f"**Product**: {product_data['name']}\n"
                        response += f"**Description**: {product_data['description']}\n"
                        response += f"**Pain Points**: {', '.join(product_data['pain_points'])}\n"
                        response += f"**Pricing**: {product_data['pricing']}\n"
                        response += f"**Target Audience**: {product_data['target_audience']}\n"
                    else:
                        response = f"❌ Failed to analyze {url}. Please try again with a different URL."
                else:
                    response = "Please provide a URL to analyze."
            else:  # RAG
                results = vector_store.similarity_search(prompt, k=5)
                context = "\n".join([doc.page_content for doc in results])
                system_prompt = """You are a helpful product analysis assistant. Using the provided context, answer the user's question clearly and concisely. 
                If the information is not available in the context, say so. Format your response using markdown for better readability."""
                
                human_prompt = f"Context from knowledge base:\n{context}\n\nUser question: {prompt}"
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=human_prompt)
                ]
                response = ChatOpenAI(model="gpt-4", temperature=0.7).invoke(messages).content
            
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response}) 