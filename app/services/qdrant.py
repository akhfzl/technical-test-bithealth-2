from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance, Query

class QdrantService:
    def __init__(self, url: str, api_key: str, collection: str, dim: int):
        self.url = url
        self.api_key = api_key
        self.collection = collection
        self.dim = dim

        self.client = QdrantClient(
            url=self.url,
            api_key=self.api_key,
        )

        self._ensure_collection()

    def _ensure_collection(self):
        try:
            return self.client.get_collection(self.collection)
        except Exception:
            return self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=self.dim,
                    distance=Distance.COSINE
                )
            )
    
    def is_healthy(self):
        try:
            info = self.client.get_collection(self.collection)
            return info is not None
        except Exception:
            return False

    def upsert_document(self, doc_id: str, vector, payload: dict):
        self.client.upsert(
            collection_name=self.collection,
            points=[PointStruct(id=doc_id, vector=vector, payload=payload)]
        )

    def search_document(self, query_vector, top_k=5):
        try:
            result = self.client.query_points(
                collection_name=self.collection,
                query=query_vector, 
                limit=top_k,
            )

            return result.points
        except Exception as e:
            print(f"Error in search_document: {e}") 
            raise

    def delete(self, doc_id: str):
        self.client.delete(
            collection_name=self.collection,
            points_selector=[doc_id]
        )

    def list_documents(self, limit=10):
        points, _ = self.client.scroll(
            collection_name=self.collection,
            limit=limit,
        )
        return points