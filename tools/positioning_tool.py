"""
Tool for generating product positioning analysis.
"""

from langchain.tools import BaseTool
from typing import Optional, Dict, Any, List
import streamlit as st
from langchain_openai import ChatOpenAI
from typing import Any
from pydantic import Field

class PositioningTool(BaseTool):
    """
    Tool for generating product positioning analysis.
    """
    
    name = "positioning_tool"
    description = """Generates a comprehensive product positioning analysis.
    Use this when the user wants to create or analyze product positioning, develop marketing strategy,
    or understand market differentiation for a feature.
    Input can be empty or contain additional context for the positioning analysis.
    """
    vector_store: Any = Field(description="Vector store for retrieving relevant information")
    llm: Any = Field(default=None, description="Language model to use")
    
    def __init__(self, vector_store, llm=None):
        """
        Initialize the positioning tool.
        
        Args:
            vector_store: The vector store to use for retrieving relevant information
            llm: Language model to use (optional)
        """
        llm = llm or ChatOpenAI(model="gpt-4", temperature=0.7)
        super().__init__(vector_store=vector_store, llm=llm)
        
    def _run(self, query: Optional[str] = None) -> str:
        """
        Generate positioning analysis.
        
        Args:
            query: Optional additional context or specific positioning question
            
        Returns:
            The generated positioning analysis as a string
        """
        try:
            feature_info = self._get_feature_info()
            
            # Gather all relevant information from vector store
            product_info = self._get_product_info()
            user_insights = self._get_user_insights()
            competitor_info = self._get_competitor_info()
            
            context = {
                'product_info': self._format_docs(product_info),
                'user_insights': self._format_docs(user_insights),
                'competitor_info': self._format_docs(competitor_info)
            }
            
            # Include the query in the prompt if provided
            additional_context = ""
            if query:
                additional_context = f"\nAdditional Request: {query}"
            
            from agents.prompts.positioning import POSITIONING_ANALYSIS_PROMPT
            
            prompt = self._format_prompt(
                POSITIONING_ANALYSIS_PROMPT,
                feature_name=feature_info['name'],
                release_date=feature_info['release_date'],
                additional_context=additional_context,
                **context
            )
            
            result = self.llm.invoke(prompt).content
            return result
        except Exception as e:
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
    
    def _format_prompt(self, template: str, **kwargs) -> str:
        """
        Format prompt template with variables.
        
        Args:
            template: The template string to format
            **kwargs: Variables to insert into the template
            
        Returns:
            The formatted prompt string
        """
        try:
            result = template.format(**kwargs)
            return result
        except Exception as e:
            raise 