from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings  
from fastapi import FastAPI
from typing import List

class VectorStoreService:
    def __init__(self, app: FastAPI):
        # Reuse the singleton Chroma client
        self.client: Chroma = app.state.chroma_client

    async def ingest_text(self, text: str, metadata: dict = None):
        """Ingest a single chunk of text."""
        metadata = metadata or {}
        doc = Document(page_content=text, metadata=metadata)
        self.client.add_documents([doc])

    async def ingest_chunks(self, chunks: List[Document]):
        """Ingest multiple pre-split Document chunks."""
        self.client.add_documents(chunks)

    async def query(self, query_text: str, k: int = 4):
        """Retrieve top-k similar documents."""
        results = self.client.similarity_search(query_text, k=k)
        return [{"text": r.page_content, "metadata": r.metadata} for r in results]
