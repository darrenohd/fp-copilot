from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
import os

class VectorStoreManager:
    @staticmethod
    def initialize():
        pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
        index_name = os.environ.get("PINECONE_INDEX_NAME")
        index = pc.Index(index_name)
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        return PineconeVectorStore(index=index, embedding=embeddings) 