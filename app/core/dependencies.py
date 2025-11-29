from fastapi import Request
from app.models import create_initial_state

def get_embedder(request: Request):
    return request.app.state.embedder

def get_qdrant(request: Request):
    return request.app.state.qdrant

def get_workflow(request: Request):
    return request.app.state.workflow

def get_initial_state():
    return create_initial_state
