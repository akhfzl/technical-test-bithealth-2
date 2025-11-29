from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
import uuid

from app.models import DocumentInput
from app.core import get_embedder, get_qdrant

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/ingest")
async def ingest_document(
    doc: DocumentInput,
    embedder=Depends(get_embedder),
    qdrant=Depends(get_qdrant)
):
    try:
        vector = embedder.generate(doc.content)
        point_id = str(uuid.uuid4())

        payload = {
            "content": doc.content,
            "metadata": doc.metadata or {},
            "ingested_at": datetime.utcnow().isoformat(),
        }

        qdrant.upsert_document(point_id, vector, payload)

        return {"id": point_id, "message": "Document ingested successfully"}
    except Exception as e:
        raise HTTPException(500, detail=f"Ingestion failed: {e}")

@router.get("/")
async def list_documents(
    limit: int = 10,
    qdrant=Depends(get_qdrant)
):
    try:
        points = qdrant.list_documents(limit)
        docs = [
            {
                "id": p.id,
                "content": p.payload["content"][:100] + "...",
                "metadata": p.payload.get("metadata", {})
            }
            for p in points
        ]
        return {"documents": docs}
    except Exception as e:
        raise HTTPException(500, detail=f"Failed to list documents: {e}")

@router.delete("/{doc_id}")
async def delete_document(doc_id: str, qdrant=Depends(get_qdrant)):
    try:
        qdrant.delete(doc_id)
        return {"message": f"Document {doc_id} deleted"}
    except Exception as e:
        raise HTTPException(500, detail=f"Deletion failed: {e}")


