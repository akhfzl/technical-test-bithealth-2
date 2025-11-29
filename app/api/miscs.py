from fastapi import APIRouter, Depends
import random, asyncio
from datetime import datetime

from app.core import get_qdrant, get_workflow

router = APIRouter(prefix="/misc", tags=["Misc"])

counter = 0

@router.get("/health")
async def health(qdrant=Depends(get_qdrant), workflow=Depends(get_workflow)):
    try:
        qdrant.is_healthy()
        return {
            "status": "healthy",
            "qdrant": "connected",
            "workflow": "ready"
        }
    except:
        return {
            "status": "unhealthy",
            "qdrant": "disconnected",
            "workflow": "ready" if workflow else "not ready"
        }

@router.get("/counter")
async def get_counter():
    global counter
    counter += 1
    return {"counter": counter}

@router.get("/chaos")
async def chaos():
    await asyncio.sleep(random.uniform(0.1, 2.0))
    return {
        "message": "Chaos mode activated",
        "value": random.randint(1, 100),
        "timestamp": datetime.utcnow().isoformat()
    }
