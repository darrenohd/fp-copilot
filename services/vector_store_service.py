"""
Service for managing the vector database.
"""

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
import os

class VectorStoreService:
    """
    Service responsible for managing the vector database.
    """
    
    @staticmethod
    def initialize():
        """
        Initialize the vector store connection.
        
        Returns:
            An initialized vector store instance
        """
        pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
        index_name = os.environ.get("PINECONE_INDEX_NAME")
        index = pc.Index(index_name)
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        return PineconeVectorStore(index=index, embedding=embeddings)
    
    def __init__(self, vector_store):
        """
        Initialize the vector store service.
        
        Args:
            vector_store: The vector store instance
        """
        self.vector_store = vector_store
    
    def similarity_search(self, query, filter=None, k=4):
        """
        Perform similarity search on the vector store.
        
        Args:
            query: The query string
            filter: Optional filter dictionary
            k: Number of results to return
        
        Returns:
            List of matching documents
        """
        return self.vector_store.similarity_search(query, filter=filter, k=k)
    
    def add_documents(self, documents):
        """
        Add documents to the vector store.
        
        Args:
            documents: List of documents to add
        """
        return self.vector_store.add_documents(documents=documents)
    
    def add_texts(self, texts, metadatas=None):
        """
        Add texts to the vector store.
        
        Args:
            texts: List of text strings to add
            metadatas: Optional list of metadata dictionaries
        """
        return self.vector_store.add_texts(texts=texts, metadatas=metadatas) 