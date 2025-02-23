from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile
import os
from langchain.schema import Document

class DocumentProcessor:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
    def process_file(self, uploaded_file, doc_type):
        """
        doc_type: One of ['requirements', 'interviews', 'strategy']
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=self._get_extension(uploaded_file)) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            loader = self._get_loader(tmp_file_path)
            documents = loader.load()
            
            # Add metadata about document type
            for doc in documents:
                doc.metadata['doc_type'] = doc_type
            
            # Split and store in vector database
            split_docs = self.text_splitter.split_documents(documents)
            self.vector_store.add_documents(documents=split_docs)
            return True
        finally:
            os.unlink(tmp_file_path)
            
    def _get_extension(self, file):
        name = file.name.lower()
        if name.endswith('.pdf'):
            return '.pdf'
        elif name.endswith('.txt'):
            return '.txt'
        return '.txt'
        
    def _get_loader(self, file_path):
        if file_path.endswith('.pdf'):
            return PyPDFLoader(file_path)
        return TextLoader(file_path)

    def process_competitor(self, competitor_data):
        """Process and store competitor analysis data"""
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
        self.vector_store.add_documents(documents=split_docs) 