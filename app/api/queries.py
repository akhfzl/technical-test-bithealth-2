from fastapi import APIRouter, Depends, HTTPException
import time

from app.models import WorkflowResult, QueryInput
from app.core import get_workflow, get_initial_state

router = APIRouter(prefix="/query", tags=["Query"])

@router.post("/", response_model=WorkflowResult)
async def query_documents(
    q: QueryInput,
    workflow=Depends(get_workflow),
    initial_state=Depends(get_initial_state)
):
    start = time.time()
  
    try:
        final_state = workflow.invoke(initial_state(q.query))
        duration = time.time() - start
        
        return WorkflowResult(
            initial_query=q.query,
            retrieved_docs=final_state["retrieved_docs"],
            final_answer=final_state["final_answer"],
            processing_time=duration
        )

    except Exception as e:
        raise HTTPException(500, detail=f"Query failed: {e}")
