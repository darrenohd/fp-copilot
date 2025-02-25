from .base import BaseAgent
from .prompts.positioning import EXTRACTION_PROMPTS
from typing import Dict, Optional, Any
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.messages import SystemMessage, HumanMessage
from utils.tracing import create_span

class ScrapingAgent(BaseAgent):
    """
    Agent responsible for scraping web pages and extracting structured data.
    """
    
    def __init__(self, vector_store, model="gpt-4", temperature=0.2):
        super().__init__(model, temperature)
        self.vector_store = vector_store
        
    def execute(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Analyze product page and extract structured data.
        
        Args:
            url: URL of the product page to analyze
            
        Returns:
            Dictionary containing structured product data or None if an error occurred
        """
        with create_span("scrape_url", {"url": url}) as span:
            try:
                page_content = self._load_page(url)
                data = self._extract_product_data(page_content, url)
                
                # Store in vector database
                self._store_product_data(data)
                
                span.set_attribute("success", True)
                return data
            except Exception as e:
                span.set_attribute("success", False)
                span.set_attribute("error", str(e))
                self._handle_error(f"Error analyzing page {url}: {str(e)}")
                return None
    
    def _load_page(self, url: str) -> str:
        """
        Load a web page and extract its content.
        
        Args:
            url: URL of the page to load
            
        Returns:
            The page content as a string
        """
        with create_span("load_page", {"url": url}) as span:
            try:
                loader = WebBaseLoader(url)
                loader.requests_kwargs = {'verify': False}  # Skip SSL verification if needed
                docs = loader.load()
                content = docs[0].page_content
                span.set_attribute("success", True)
                span.set_attribute("content_length", len(content))
                return content
            except Exception as e:
                span.set_attribute("success", False)
                span.set_attribute("error", str(e))
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
        with create_span("extract_product_data", {"content_length": len(content)}) as span:
            try:
                data = {
                    'name': self._extract_field(content, 'name'),
                    'description': self._extract_field(content, 'description'),
                    'pain_points': self._extract_field(content, 'pain_points').split(','),
                    'pricing': self._extract_field(content, 'pricing'),
                    'target_audience': self._extract_field(content, 'target_audience'),
                    'url': url
                }
                span.set_attribute("success", True)
                return data
            except Exception as e:
                span.set_attribute("success", False)
                span.set_attribute("error", str(e))
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
        with create_span(f"extract_field_{field}", {"content_length": len(content)}) as span:
            try:
                prompt = EXTRACTION_PROMPTS[field]
                
                messages = [
                    SystemMessage(content="""You are a precise data extraction specialist with expertise in product marketing analysis.
                    Your responses should be concise and directly address the requested information.
                    Avoid speculation and stick to information present in the content."""),
                    HumanMessage(content=prompt.format(text=content))
                ]
                
                result = self.llm.invoke(messages).content.strip()
                span.set_attribute("success", True)
                return result
            except Exception as e:
                span.set_attribute("success", False)
                span.set_attribute("error", str(e))
                raise
                
    def _store_product_data(self, data: Dict[str, Any]) -> None:
        """
        Store product data in the vector database.
        
        Args:
            data: Dictionary containing structured product data
        """
        with create_span("store_product_data", {"product": data.get('name', 'unknown')}) as span:
            try:
                content = f"""
                Product: {data['name']}
                Description: {data['description']}
                Pain Points Solved: {', '.join(data['pain_points'])}
                Pricing: {data['pricing']}
                Target Audience: {data['target_audience']}
                Source URL: {data['url']}
                """
                
                self.vector_store.add_texts(
                    texts=[content],
                    metadatas=[{'type': 'product_page', 'url': data['url']}]
                )
                span.set_attribute("success", True)
            except Exception as e:
                span.set_attribute("success", False)
                span.set_attribute("error", str(e))
                raise 