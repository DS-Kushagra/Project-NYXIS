from typing import Dict, Any, List
from fastapi import FastAPI
from .vector_store import VectorStoreService
from .chat_service import ChatService

def get_search_docs_tool(app: FastAPI):
    async def search_docs(query: str, k: int = 4) -> List[Dict[str, Any]]:
        store = VectorStoreService(app)
        return await store.query(query, k)
    return {
        "name": "search_docs",
        "description": "Use this to find relevant document chunks. Input: a search query string.",
        "func": search_docs
    }

def get_chat_rag_tool(app: FastAPI):
    async def chat_rag(prompt: str, k: int = 4) -> str:
        chat = ChatService(app)
        return await chat.chat(prompt, k)
    return {
        "name": "chat_rag",
        "description": "Use this to answer a question given context. Input: a question string.",
        "func": chat_rag
    }
