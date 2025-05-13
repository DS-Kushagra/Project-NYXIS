import os
import tempfile
from fastapi import APIRouter, Request, File, UploadFile, HTTPException
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from ..services.vector_store import VectorStoreService
from langchain.schema import Document

router = APIRouter(prefix="/api/ingest-file", tags=["ingest-file"])

@router.post("")
async def ingest_file(
    request: Request,
    file: UploadFile = File(...)
):
    # 1. Save uploaded bytes to a temp file
    suffix = os.path.splitext(file.filename)[1]
    try:
        contents = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        # 2. Choose loader by extension
        if suffix.lower() == ".pdf":
            loader = PyPDFLoader(tmp_path)
        elif suffix.lower() in (".txt", ".md"):
            loader = TextLoader(tmp_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # 3. Load & split
        docs: List[Document] = loader.load()
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks: List[Document] = splitter.split_documents(docs)

        # 4. Ingest chunks
        store = VectorStoreService(request.app)
        await store.ingest_chunks(chunks)

        return {"status": "ingested", "chunks": len(chunks)}

    except HTTPException:
        raise
    except Exception as e:
        # Log or print e if you like
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 5. Clean up temp file
        try:
            os.remove(tmp_path)
        except Exception:
            pass
