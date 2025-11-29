from app.services import WorkflowService
from app.models import WorkflowResult

class MockEmbedder:
    def generate(self, text: str):
        return [0.1, 0.2, 0.3]  

class MockQdrant:
    def search_document(self, vector, top_k=5):
        return [
            {
                "id": "123",
                "content": "Mock document for testing",
                "metadata": {},
                "score": 0.88
            }
        ]


def test_workflow_returns_docs():
    embedder = MockEmbedder()
    qdrant = MockQdrant()

    workflow = WorkflowService(embedder, qdrant).workflow
    initial_state = {
        "query": "document",
        "retrieved_docs": [],
        "final_answer": "",
        "processing_steps": [],
        "error": None
    }

    final_state = workflow.invoke(initial_state)
    result = WorkflowResult(
            initial_query=initial_state["query"],
            retrieved_docs=final_state["retrieved_docs"],
            final_answer=final_state["final_answer"],
            processing_time='1.2'
    )
    
    assert len(result["retrieved_docs"]) == 1
    assert result["final_answer"].startswith("Top doc:")
