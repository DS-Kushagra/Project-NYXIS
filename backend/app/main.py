from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

from .routers.ingest import router as ingest_router
from .routers.query  import router as query_router
from .routers.ingest_file import router as file_ingest_router
from .routers.chat import router as chat_router
from .routers.agent import router as agent_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.chroma_client = Chroma(
        persist_directory="chroma_db",
        embedding_function=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    )
    yield
    await app.state.chroma_client.close()

app = FastAPI(title="Project-NYXIS", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only — lock this down for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(ingest_router)
app.include_router(query_router)
app.include_router(file_ingest_router)
app.include_router(chat_router)
app.include_router(agent_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
