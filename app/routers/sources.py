from fastapi import APIRouter
from app.database import get_db
from app.agents.qa_compliance import QAComplianceAgent

router = APIRouter(prefix="/api/sources", tags=["Sources"])
qa_agent = QAComplianceAgent()

@router.get("")
@router.get("/")
async def list_sources():
    with get_db() as conn:
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT s.*, COUNT(q.id) as question_count 
            FROM sources s
            LEFT JOIN questions q ON s.id = q.source_name OR s.name = q.source_name
            GROUP BY s.id
        """).fetchall()
        return [dict(r) for r in rows]

@router.post("/audit")
async def run_compliance_audit():
    with get_db() as conn:
        audit_result = qa_agent.audit(conn)
    return audit_result
