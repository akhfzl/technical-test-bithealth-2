def create_initial_state(query: str):
    return {
        "query": query,
        "retrieved_docs": [],
        "final_answer": "",
        "processing_steps": [],
        "error": None
    }
