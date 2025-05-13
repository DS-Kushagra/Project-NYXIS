from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from ..services.chat_service import ChatService

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str = Field(..., example="What is FastAPI?")
    k: Optional[int] = Field(4, ge=1, le=10)

class ChatResponse(BaseModel):
    reply: str

@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: Request, req: ChatRequest):
    service = ChatService(request.app)
    try:
        reply = await service.chat(req.message, req.k)
        return ChatResponse(reply=reply)
    except Exception:
        raise HTTPException(status_code=500, detail="Chat generation failed")
