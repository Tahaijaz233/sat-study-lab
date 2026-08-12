from fastapi import APIRouter
router = APIRouter(prefix="/api/agents")

@router.get("/status")
def get_status():
    return {"status": "ok"}
