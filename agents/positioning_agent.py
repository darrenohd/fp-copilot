from .base import BaseAgent
from .prompts.positioning import POSITIONING_ANALYSIS_PROMPT
from typing import Dict, List, Any
import streamlit as st

class PositioningAgent(BaseAgent):
    def __init__(self, vector_store, model="gpt-4", temperature=0.7):
        super().__init__(model, temperature)
        self.vector_store = vector_store
        
    def execute(self) -> str:
        """Generate positioning analysis"""
        feature_info = self._get_feature_info()
        context = self._gather_context()
        
        prompt = self._format_prompt(
            POSITIONING_ANALYSIS_PROMPT,
            feature_name=feature_info['name'],
            release_date=feature_info['release_date'],
            **context
        )
        
        return self.llm.invoke(prompt).content
        
    def _gather_context(self) -> Dict[str, str]:
        """Gather all necessary context for analysis"""
        return {
            'product_info': self._get_product_info(),
            'user_insights': self._get_user_insights(),
            'competitor_info': self._get_competitor_info()
        }
    
    def _get_feature_info(self) -> Dict[str, Any]:
        """Get feature information from session state"""
        return st.session_state.get('feature_info', {
            'name': 'Unnamed Feature',
            'release_date': 'TBD'
        })
    