from langgraph.graph import StateGraph, END

class RAGWorkflowBuilder:
    def __init__(self, embedder, qdrant):
        self.embedder = embedder
        self.qdrant = qdrant

    def retrieve_node(self, state):
        query = state["query"]
        vector = self.embedder.generate(query)
        points = self.qdrant.search_document(vector, top_k=5)
       
        docs = []
        for p in points:
            docs.append({
                "id": str(p.id), 
                "content": str(p.payload.get("content", "")), 
                "metadata": dict(p.payload.get("metadata", {})),  
                "score": float(p.score) if p.score is not None else None  
            })

        state["retrieved_docs"] = docs
        
        return state

    def answer_node(self, state):
        docs = state["retrieved_docs"]

        if not docs:
            state["final_answer"] = "No documents found."
        else:
            best = docs[0]
            state["final_answer"] = f"Top doc: {best['content'][:200]}..."

        return state

    def build(self):
        graph = StateGraph(dict)

        graph.add_node("retrieve", self.retrieve_node)
        graph.add_node("answer", self.answer_node)

        graph.set_entry_point("retrieve")
        graph.add_edge("retrieve", "answer")
        graph.add_edge("answer", END)

        return graph.compile()
