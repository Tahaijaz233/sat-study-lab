from fastapi import APIRouter
from app.database import get_db
from app.agents.analytics_agent import AnalyticsAgent

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])
analytics_agent = AnalyticsAgent()

@router.get("/summary")
async def get_summary():
    """Returns real-time analytics summary from user attempts."""
    with get_db() as conn:
        stats = analytics_agent.compute_dashboard_stats(conn)
    return stats

@router.get("/weak-areas")
async def get_weak_areas():
    """Returns topics with accuracy < 70%."""
    with get_db() as conn:
        weak_topics = analytics_agent.get_weak_topics(conn)
    return weak_topics
