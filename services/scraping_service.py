"""
Service for scraping web pages and extracting structured data.
"""

from typing import Dict, Optional, Any
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from agents.prompts.positioning import EXTRACTION_PROMPTS

class ScrapingService:
    """
    Service responsible for scraping web pages and extracting structured data.
    """
    
    def __init__(self, llm=None):
        """
        Initialize the scraping service.
        
        Args:
            llm: Language model to use for extraction (optional)
        """
        self.llm = llm or ChatOpenAI(model="gpt-4", temperature=0.2)
        
    def analyze_website(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Analyze product page and extract structured data.
        
        Args:
            url: URL of the product page to analyze
            
        Returns:
            Dictionary containing structured product data or None if an error occurred
        """
        try:
            page_content = self._load_page(url)
            data = self._extract_product_data(page_content, url)
            return data
        except Exception as e:
            print(f"Error analyzing page {url}: {str(e)}")
            return None
    
    def _load_page(self, url: str) -> str:
        """
        Load a web page and extract its content.
        
        Args:
            url: URL of the page to load
            
        Returns:
            The page content as a string
        """
        try:
            loader = WebBaseLoader(url)
            loader.requests_kwargs = {'verify': False}  # Skip SSL verification if needed
            docs = loader.load()
            content = docs[0].page_content
            return content
        except Exception as e:
            raise
            
    def _extract_product_data(self, content: str, url: str) -> Dict[str, Any]:
        """
        Extract structured data from page content.
        
        Args:
            content: The page content to analyze
            url: URL of the page
            
        Returns:
            Dictionary containing structured product data
        """
        try:
            data = {
                'name': self._extract_field(content, 'name'),
                'description': self._extract_field(content, 'description'),
                'pain_points': self._extract_field(content, 'pain_points').split(','),
                'pricing': self._extract_field(content, 'pricing'),
                'target_audience': self._extract_field(content, 'target_audience'),
                'url': url
            }
            return data
        except Exception as e:
            raise
        
    def _extract_field(self, content: str, field: str) -> str:
        """
        Extract specific field using appropriate prompt.
        
        Args:
            content: The content to analyze
            field: The field to extract
            
        Returns:
            The extracted field value as a string
        """
        try:
            prompt = EXTRACTION_PROMPTS[field]
            
            messages = [
                SystemMessage(content="""You are a precise data extraction specialist with expertise in product marketing analysis.
                Your responses should be concise and directly address the requested information.
                Avoid speculation and stick to information present in the content."""),
                HumanMessage(content=prompt.format(text=content))
            ]
            
            result = self.llm.invoke(messages).content.strip()
            return result
        except Exception as e:
            raise 