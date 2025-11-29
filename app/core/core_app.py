from app.services import EmbeddingService, QdrantService, WorkflowService
from app.config import settings

def init_services():
    embedder = EmbeddingService(dim=settings.EMBED_DIM)

    qdrant = QdrantService(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        collection=settings.QDRANT_COLLECTION,
        dim=settings.EMBED_DIM,
    )

    workflow = WorkflowService(embedder, qdrant).workflow

    return embedder, qdrant, workflow
