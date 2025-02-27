"""
Feature Positioning Copilot Services Module

This module contains service classes that handle core functionality like
document processing, web scraping, and vector store management.
"""

from .document_service import DocumentService
from .scraping_service import ScrapingService

__all__ = [
    'DocumentService',
    'ScrapingService',
] 