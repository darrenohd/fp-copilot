"""
Tool for extracting structured data from competitor websites.
"""

from langchain.tools import BaseTool
from typing import Optional, Dict, Any
import re
from pydantic import Field

class ScrapingTool(BaseTool):
    """
    Tool for extracting structured data from competitor websites.
    """
    
    name = "scraping_tool"
    description = """Extracts structured data from competitor websites.
    Use this when the user wants to analyze or scrape information from a specific URL.
    Input should be a valid URL to analyze.
    """
    
    scraping_service: Any = Field(description="Service for scraping websites")
    document_service: Any = Field(description="Service for processing and storing scraped data")
    
    def __init__(self, scraping_service, document_service):
        """
        Initialize the scraping tool.
        
        Args:
            scraping_service: Service for scraping websites
            document_service: Service for processing and storing scraped data
        """
        super().__init__(scraping_service=scraping_service, document_service=document_service)
    
    def _run(self, url: str) -> str:
        """
        Analyze a website and extract structured data.
        
        Args:
            url: URL of the website to analyze
            
        Returns:
            Formatted analysis result
        """
        try:
            # Check if input is a valid URL
            if not self._is_valid_url(url):
                return "Please provide a valid URL to analyze."
            
            # Analyze the website
            product_data = self.scraping_service.analyze_website(url)
            if not product_data:
                return f"Failed to analyze {url}. Please try again with a different URL."
            
            # Store in vector database
            self.document_service.process_competitor(product_data)
            
            # Format result
            response = f"✅ Successfully analyzed {url}. Here's what I found:\n\n"
            response += f"**Product**: {product_data['name']}\n"
            response += f"**Description**: {product_data['description']}\n"
            response += f"**Pain Points**: {', '.join(product_data['pain_points'])}\n"
            response += f"**Pricing**: {product_data['pricing']}\n"
            response += f"**Target Audience**: {product_data['target_audience']}\n"
            
            return response
        except Exception as e:
            return f"Error analyzing website: {str(e)}"
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Check if a string is a valid URL.
        
        Args:
            url: String to check
            
        Returns:
            True if valid URL, False otherwise
        """
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None 