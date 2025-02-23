from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile
import os

class DocumentProcessor:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=400,
            length_function=len,
            is_separator_regex=False,
        )
        self._loaders = {
            'pdf': PyPDFLoader,
            'txt': TextLoader,
            'csv': CSVLoader
        }

    def get_supported_formats(self):
        return list(self._loaders.keys())

    def process_file(self, uploaded_file):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            loader = PyPDFLoader(tmp_file_path)
            raw_documents = loader.load()
            documents = self.text_splitter.split_documents(raw_documents)
            uuids = [f"id{i}" for i in range(len(documents))]
            self.vector_store.add_documents(documents=documents, ids=uuids)
            return True
        finally:
            os.unlink(tmp_file_path)

    def process_text(self, text, metadata=None):
        if metadata is None:
            metadata = {}
        
        documents = self.text_splitter.create_documents([text], metadatas=[metadata])
        uuids = [f"id{i}" for i in range(len(documents))]
        self.vector_store.add_documents(documents=documents, ids=uuids)
        return True 