"""
Tool for retrieving information from the knowledge base to answer questions.
"""

from langchain.tools import BaseTool
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from typing import Any
from pydantic import Field

class RAGTool(BaseTool):
    """
    Tool for retrieving information from the knowledge base to answer questions.
    """
    
    name = "rag_tool"
    description = """Retrieves information from the knowledge base to answer questions.
    Use this for general questions about the product, market, or when specific information might be in the database.
    Input should be the question to answer.
    """
    
    vector_store: Any = Field(description="Vector store for retrieving relevant information")
    llm: Any = Field(default=None, description="Language model to use")
    
    def __init__(self, vector_store, llm=None):
        """
        Initialize the RAG tool.
        
        Args:
            vector_store: The vector store to use for retrieving relevant information
            llm: Language model to use (optional)
        """
        llm = llm or ChatOpenAI(model="gpt-4", temperature=0.7)
        super().__init__(vector_store=vector_store, llm=llm)
    
    def _run(self, query: str) -> str:
        """
        Answer a question using the knowledge base.
        
        Args:
            query: The question to answer
            
        Returns:
            The answer from the knowledge base
        """
        try:
            # Retrieve relevant documents
            results = self.vector_store.similarity_search(query, k=5)
            context = "\n".join([doc.page_content for doc in results])
            
            # Format prompt with context
            system_prompt = """You are a helpful product analysis assistant. Using the provided context, answer the user's question clearly and concisely. 
            If the information is not available in the context, say so. Format your response using markdown for better readability."""
            
            human_prompt = f"Context from knowledge base:\n{context}\n\nUser question: {query}"
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]
            
            # Generate response
            response = self.llm.invoke(messages).content
            return response
        except Exception as e:
            return f"Error retrieving information: {str(e)}" 