from app.workflows import RAGWorkflowBuilder

class WorkflowService:
    def __init__(self, embedder, qdrant):
        builder = RAGWorkflowBuilder(embedder, qdrant)
        self.workflow = builder.build()

    def run(self, initial_state):
        return self.workflow.invoke(initial_state)
