from .base import BaseAgent
from .prompts.positioning import EXTRACTION_PROMPTS
from typing import Dict, Optional, Any
from langchain_community.document_loaders import WebBaseLoader

class ScrapingAgent(BaseAgent):
    def __init__(self, vector_store, model="gpt-4", temperature=0.2):
        super().__init__(model, temperature)
        self.vector_store = vector_store
        
    def execute(self, url: str) -> Optional[Dict[str, Any]]:
        """Analyze product page and extract structured data"""
        try:
            page_content = self._load_page(url)
            return self._extract_product_data(page_content, url)
        except Exception as e:
            self._handle_error(f"Error analyzing page {url}: {str(e)}")
            return None
            
    def _extract_product_data(self, content: str, url: str) -> Dict[str, Any]:
        """Extract structured data from page content"""
        return {
            'name': self._extract_field(content, 'name'),
            'description': self._extract_field(content, 'description'),
            'pain_points': self._extract_field(content, 'pain_points').split(','),
            'pricing': self._extract_field(content, 'pricing'),
            'target_audience': self._extract_field(content, 'target_audience'),
            'url': url
        }
        
    def _extract_field(self, content: str, field: str) -> str:
        """Extract specific field using appropriate prompt"""
        prompt = EXTRACTION_PROMPTS[field]
        return self._format_prompt(prompt, text=content) 