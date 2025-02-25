from .base import BaseAgent
from .prompts.positioning import POSITIONING_ANALYSIS_PROMPT
from typing import Dict, List, Any
import streamlit as st
from utils.tracing import create_span

class PositioningAgent(BaseAgent):
    """
    Agent responsible for generating product positioning analysis.
    """
    
    def __init__(self, vector_store, model="gpt-4", temperature=0.7):
        super().__init__(model, temperature)
        self.vector_store = vector_store
        
    def execute(self) -> str:
        """
        Generate positioning analysis.
        
        Returns:
            The generated positioning analysis as a string
        """
        with create_span("generate_positioning") as span:
            try:
                feature_info = self._get_feature_info()
                span.set_attribute("feature_name", feature_info['name'])
                
                # Gather all relevant information from vector store
                product_info = self._get_product_info()
                user_insights = self._get_user_insights()
                competitor_info = self._get_competitor_info()
                
                context = {
                    'product_info': self._format_docs(product_info),
                    'user_insights': self._format_docs(user_insights),
                    'competitor_info': self._format_docs(competitor_info)
                }
                
                prompt = self._format_prompt(
                    POSITIONING_ANALYSIS_PROMPT,
                    feature_name=feature_info['name'],
                    release_date=feature_info['release_date'],
                    **context
                )
                
                result = self.llm.invoke(prompt).content
                span.set_attribute("success", True)
                return result
            except Exception as e:
                span.set_attribute("success", False)
                span.set_attribute("error", str(e))
                self._handle_error(f"Error generating positioning: {str(e)}")
                return f"Error generating positioning analysis: {str(e)}"
    
    def _get_feature_info(self) -> Dict[str, Any]:
        """
        Get feature information from session state.
        
        Returns:
            Dictionary containing feature information
        """
        return st.session_state.get('feature_info', {
            'name': 'Unnamed Feature',
            'release_date': 'TBD'
        })
        
    def _get_product_info(self):
        """
        Get product information from vector store.
        
        Returns:
            List of documents containing product information
        """
        return self.vector_store.similarity_search(
            "What are our product's key features and benefits?",
            filter={"doc_type": "requirements"}
        )
        
    def _get_user_insights(self):
        """
        Get user insights from vector store.
        
        Returns:
            List of documents containing user insights
        """
        return self.vector_store.similarity_search(
            "What are the main user pain points and needs?",
            filter={"doc_type": "interviews"}
        )
        
    def _get_competitor_info(self):
        """
        Get competitor information from vector store.
        
        Returns:
            List of documents containing competitor information
        """
        return self.vector_store.similarity_search(
            "What are competitor strengths and weaknesses?",
            filter={"type": "product_page"}
        )
        
    def _format_docs(self, docs):
        """
        Format documents for inclusion in prompts.
        
        Args:
            docs: List of documents to format
            
        Returns:
            Formatted document content as a string
        """
        return "\n".join([doc.page_content for doc in docs])
    