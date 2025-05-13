from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from ..services.vector_store import VectorStoreService

router = APIRouter(prefix="/api/ingest", tags=["ingest"])

class IngestRequest(BaseModel):
    text: str
    metadata: dict = {}

@router.post("", status_code=201)
async def ingest(req: IngestRequest, request: Request):
    store = VectorStoreService(request.app)
    try:
        await store.ingest_text(req.text, req.metadata)
        return {"status": "Ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
