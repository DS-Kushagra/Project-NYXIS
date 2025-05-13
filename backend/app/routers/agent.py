# backend/app/routers/agent.py

import logging
import anyio
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
from typing import List, Any

from langchain.agents import initialize_agent, Tool, AgentType
from langchain.llms import HuggingFacePipeline
from transformers import pipeline as hf_pipeline
from langchain.text_splitter import RecursiveCharacterTextSplitter

from ..services.agent_tools import get_search_docs_tool, get_chat_rag_tool
from ..services.vector_store import VectorStoreService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/agent", tags=["agent"])

class AgentRequest(BaseModel):
    goal: str = Field(..., example="Find and summarize mentions of 'LangChain' in my docs.")

class AgentStep(BaseModel):
    tool: str
    input: Any
    output: Any

class AgentResponse(BaseModel):
    final_output: str
    steps: List[AgentStep]

@router.post("", response_model=AgentResponse)
async def run_agent(request: Request, req: AgentRequest):
    # 1. Build tools
    search_tool = get_search_docs_tool(request.app)
    chat_tool   = get_chat_rag_tool(request.app)
    tools = [
        Tool(name=search_tool["name"], func=search_tool["func"], description=search_tool["description"]),
        Tool(name=chat_tool["name"],   func=chat_tool["func"],   description=chat_tool["description"]),
    ]

    # 2. Retrieve and chunk context
    store = VectorStoreService(request.app)
    docs = await store.query(req.goal, k=4)
    texts = [d["text"] for d in docs]
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_chunks = splitter.split_text("\n\n".join(texts))
    context = "\n\n".join(all_chunks[:3])  # limit to first 3 chunks

    # 3. Create HF LLM wrapper
    hf_gen = hf_pipeline(
        "text2text-generation",
        model="google/flan-t5-small",
        device=0,
        max_length=256,
        do_sample=False,
    )
    llm = HuggingFacePipeline(pipeline=hf_gen)

    # 4. Initialize chat-style agent
    agent = initialize_agent(
        tools,
        llm=llm,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )

    # 5. Run the agent
    try:
        prompt = f"Context:\n{context}\nQuestion: {req.goal}"
        if hasattr(agent, "ainvoke"):
            raw_result = await agent.ainvoke(prompt)
        else:
            raw_result = await anyio.to_thread.run_sync(lambda: agent.invoke(prompt))
    except Exception as e:
        logger.error("Agent execution failed", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Agent error: {e}")

    # 6. Coerce final output to string 
    final_text = (
        raw_result.get("output") if isinstance(raw_result, dict) else str(raw_result)
    )

    return AgentResponse(final_output=final_text, steps=[])
