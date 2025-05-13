from fastapi import APIRouter, Request, HTTPException
from typing import List
from pydantic import BaseModel

from ..services.vector_store import VectorStoreService

router = APIRouter(prefix="/api/query", tags=["query"])

class QueryResponse(BaseModel):
    text: str
    metadata: dict

@router.get("", response_model=List[QueryResponse])
async def query(request: Request, q: str, k: int = 4):
    store = VectorStoreService(request.app)
    try:
        results = await store.query(q, k)  # Should return List[dict]
        # Parse into Pydantic models
        return [QueryResponse.parse_obj(r) for r in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
