# backend/app/services/chat_service.py

from typing import List
from fastapi import FastAPI
from transformers import pipeline, AutoTokenizer, Pipeline
from .vector_store import VectorStoreService
import logging

logger = logging.getLogger(__name__)

class ChatService:
    MODEL_NAME = "google/flan-t5-small"
    MAX_INPUT_TOKENS = 512
    RESERVED_OUTPUT_TOKENS = 128  # leave room for the model's reply

    def __init__(self, app: FastAPI):
        self.store = VectorStoreService(app)
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
        self.generator: Pipeline = pipeline(
            "text2text-generation",
            model=self.MODEL_NAME,
            device=-1  # CPU
        )

    async def chat(self, query: str, k: int = 4) -> str:
        # 1. Retrieve top-k chunks
        docs = await self.store.query(query, k)

        # 2. Build context with token‑budgeting
        selected_chunks: List[str] = []
        current_tokens = 0

        for chunk in docs:
            tokens = self.tokenizer.tokenize(chunk["text"])
            if current_tokens + len(tokens) > self.MAX_INPUT_TOKENS - self.RESERVED_OUTPUT_TOKENS:
                break
            selected_chunks.append(chunk["text"])
            current_tokens += len(tokens)

        context = "\n\n".join(selected_chunks)
        prompt = (
            "You are Project‑NYXIS, an AI assistant. "
            "Use the following context to answer the question.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\n"
            "Answer:"
        )

        # 3. Generate
        try:
            outputs = self.generator(
                prompt,
                max_length=self.MAX_INPUT_TOKENS,
                do_sample=False,
            )
            return outputs[0]["generated_text"]
        except Exception as e:
            logger.error(f"Generation error: {e}")
            raise

