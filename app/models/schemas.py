from typing import Dict, List, Any, Optional
from pydantic import BaseModel

class DocumentInput(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None

class QueryInput(BaseModel):
    query: str
    top_k: int = 5

class DocumentSchema(BaseModel):
    id: Optional[str] = None
    content: str = ""
    metadata: Dict[str, Any] = {}
    score: Optional[float] = None

class WorkflowResult(BaseModel):
    initial_query: str
    retrieved_docs: List[DocumentSchema]   
    final_answer: str
    processing_time: float
