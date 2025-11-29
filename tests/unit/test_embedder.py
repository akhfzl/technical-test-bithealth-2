from app.services import EmbeddingService as Embedder

def test_embedder_output_dimension():
    embedder = Embedder(dim=384)
    vec = embedder.generate("hello world")

    assert isinstance(vec, list)
    assert len(vec) == 384
