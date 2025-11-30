from fastapi.testclient import TestClient
from app.main import app

class MockEmbedder:
    def generate(self, text: str):
        return [0.1, 0.2, 0.3]

class MockQdrant:
    def search_document(self, vector, top_k=5):
        return [
            {
                "id": "1",
                "content": "Integration mock doc",
                "metadata": {},
                "score": 0.5
            }
        ]

app.dependency_overrides = {}

from app.core.dependencies import get_embedder, get_qdrant

app.dependency_overrides[get_embedder] = lambda: MockEmbedder()
app.dependency_overrides[get_qdrant] = lambda: MockQdrant()

client = TestClient(app)

def test_query_endpoint():
    res = client.post("/query", json={"query": "Kecerdasan Buatan"})
    assert res.status_code == 200
    data = res.json()

    assert len(data["retrieved_docs"]) == 4
    assert data["retrieved_docs"][0]["content"] == "Kecerdasan Buatan (AI) terbentuk dari keinginan manusia untuk membuat mesin yang dapat berpikir dan belajar seperti manusia. Perjalanan ini dimulai dari logika dan matematika, ketika para ilmuwan menemukan bahwa proses berpikir bisa direpresentasikan dengan simbol dan aturan. Dari sini lahir komputer, yang mampu menjalankan instruksi dengan cepat. Selanjutnya, peneliti mulai merancang algoritma yang dapat mengenali pola, mengambil keputusan, dan belajar dari data. Seiring berkembangnya teknologi dan meningkatnya kemampuan komputasi, AI berevolusi dari aturan sederhana menjadi model pembelajaran mesin dan akhirnya ke deep learning, yang meniru cara kerja jaringan saraf manusia."
