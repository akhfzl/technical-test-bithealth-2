from app.services import QdrantService

class DummyClient:
    def query_points(self, *args, **kwargs):
        class Result:
            points = [{"id": "1", "payload": {"content": "abc"}, "score": 0.9}]
        return Result()

def test_qdrant_search_mock(monkeypatch):
    qdrant = QdrantService(
        url="http://mock",
        api_key="mock",
        collection="test",
        dim=3
    )

    # Mock client
    qdrant.client = DummyClient()

    results = qdrant.search_document([0.1, 0.2, 0.3])

    assert len(results) == 1
    assert results[0]["payload"]["content"] == "abc"
