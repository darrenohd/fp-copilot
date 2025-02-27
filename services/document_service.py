"""
Service for processing various document types and storing them
in the vector database.
"""

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile
import os
from langchain.schema import Document
from typing import Dict, Any, List, Optional
from utils.tracing import create_span

class DocumentService:
    """
    Service responsible for processing various document types and storing them
    in the vector database.
    """
    
    def __init__(self, vector_store):
        """
        Initialize the document service.
        
        Args:
            vector_store: The vector store to use for document storage
        """
        self.vector_store = vector_store
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def process_file(self, uploaded_file, doc_type: str) -> bool:
        """
        Process a document file and store it in the vector database.
        
        Args:
            uploaded_file: The file to process
            doc_type: The type of document ('requirements', 'interviews', 'strategy')
            
        Returns:
            True if processing was successful, False otherwise
        """
        with create_span("process_file", {
            "doc_type": doc_type,
            "filename": uploaded_file.name
        }) as span:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=self._get_extension(uploaded_file)) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                loader = self._get_loader(tmp_file_path)
                documents = loader.load()
                
                # Add metadata about document type
                for doc in documents:
                    doc.metadata['doc_type'] = doc_type
                
                # Split and store in vector database
                split_docs = self.text_splitter.split_documents(documents)
                self.vector_store.add_documents(documents=split_docs)
                
                span.set_attribute("success", True)
                span.set_attribute("document_count", len(documents))
                span.set_attribute("chunk_count", len(split_docs))
                
                return True
            except Exception as e:
                span.set_attribute("success", False)
                span.set_attribute("error", str(e))
                print(f"Error processing file: {str(e)}")
                return False
            finally:
                try:
                    os.unlink(tmp_file_path)
                except:
                    pass
            
    def _get_extension(self, file) -> str:
        """
        Get the file extension from a file object.
        
        Args:
            file: The file object
            
        Returns:
            The file extension as a string
        """
        name = file.name.lower()
        if name.endswith('.pdf'):
            return '.pdf'
        elif name.endswith('.txt'):
            return '.txt'
        return '.txt'
        
    def _get_loader(self, file_path: str):
        """
        Get the appropriate document loader for a file path.
        
        Args:
            file_path: The path to the file
            
        Returns:
            A document loader instance
        """
        if file_path.endswith('.pdf'):
            return PyPDFLoader(file_path)
        return TextLoader(file_path)

    def process_competitor(self, competitor_data: Dict[str, Any]) -> bool:
        """
        Process and store competitor analysis data.
        
        Args:
            competitor_data: Dictionary containing competitor data
            
        Returns:
            True if processing was successful, False otherwise
        """
        with create_span("process_competitor", {
            "competitor": competitor_data.get('name', 'unknown')
        }) as span:
            try:
                # Create a document from competitor data
                content = f"""
                Product Name: {competitor_data['name']}
                Description: {competitor_data['description']}
                Pain Points: {', '.join(competitor_data['pain_points'])}
                Pricing: {competitor_data['pricing']}
                Target Audience: {competitor_data['target_audience']}
                """
                
                doc = Document(
                    page_content=content,
                    metadata={
                        'doc_type': 'competitor',
                        'source': 'product_page'
                    }
                )
                
                # Split and store in vector database
                split_docs = self.text_splitter.split_documents([doc])
                
                # Add separate span for embeddings
                with create_span("create_embeddings", {
                    "doc_type": "competitor",
                    "competitor": competitor_data.get('name', 'unknown'),
                    "chunk_count": len(split_docs)
                }) as embed_span:
                    self.vector_store.add_documents(documents=split_docs)
                    embed_span.set_attribute("success", True)
                
                span.set_attribute("success", True)
                return True
            except Exception as e:
                span.set_attribute("success", False)
                span.set_attribute("error", str(e))
                print(f"Error processing competitor data: {str(e)}")
                return False 