from fastapi import FastAPI

from app.api import documents_router, query_router, misc_router
from app.core import init_services

app = FastAPI(title="Refactored LangGraph + Qdrant API", version="1.0")

embedder, qdrant, workflow = init_services()

app.state.embedder = embedder
app.state.qdrant = qdrant
app.state.workflow = workflow

app.include_router(documents_router)
app.include_router(query_router)
app.include_router(misc_router)

@app.get("/")
def root():
    return {"message": "API Ready"}
