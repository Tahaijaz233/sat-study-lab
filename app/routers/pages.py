from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import config
from app.database import get_db
from app.agents.analytics_agent import AnalyticsAgent

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
analytics_agent = AnalyticsAgent()

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    stats = {}
    try:
        with get_db() as conn:
            stats = analytics_agent.compute_dashboard_stats(conn)
    except Exception as e:
        print(f"[Dashboard Error] {e}")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"stats": stats}
    )

@router.get("/papers", response_class=HTMLResponse)
async def practice_papers(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="papers.html",
        context={"desmos_api_key": config.DESMOS_API_KEY}
    )

@router.get("/bank", response_class=HTMLResponse)
async def question_bank(request: Request):
    return templates.TemplateResponse(request=request, name="bank.html", context={})

@router.get("/vocab", response_class=HTMLResponse)
async def vocab_center(request: Request):
    return templates.TemplateResponse(request=request, name="vocab.html", context={})

@router.get("/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request):
    stats = {}
    weak_areas = []
    try:
        with get_db() as conn:
            stats = analytics_agent.compute_dashboard_stats(conn)
            weak_areas = analytics_agent.get_weak_topics(conn)
    except Exception as e:
        print(f"[Analytics Error] {e}")

    return templates.TemplateResponse(
        request=request, 
        name="analytics.html", 
        context={"stats": stats, "weak_areas": weak_areas}
    )

@router.get("/sources", response_class=HTMLResponse)
async def sources_page(request: Request):
    sources_list = []
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            rows = cursor.execute("SELECT * FROM sources").fetchall()
            sources_list = [dict(r) for r in rows]
    except Exception as e:
        print(f"[Sources Error] {e}")

    return templates.TemplateResponse(
        request=request, 
        name="sources.html", 
        context={"sources": sources_list}
    )

@router.get("/courses", response_class=HTMLResponse)
async def courses_page(request: Request):
    courses_list = []
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            rows = cursor.execute("""
                SELECT c.*, 
                       (SELECT count(*) FROM course_modules cm WHERE cm.course_id = c.id) as module_count
                FROM courses c
            """).fetchall()
            courses_list = [dict(r) for r in rows]
    except Exception as e:
        print(f"[Courses Error] {e}")

    return templates.TemplateResponse(
        request=request, 
        name="courses.html", 
        context={"courses": courses_list}
    )

@router.get("/courses/{course_id}", response_class=HTMLResponse)
async def course_detail_page(request: Request, course_id: str):
    course = None
    modules = []
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            c_row = cursor.execute("SELECT * FROM courses WHERE id = ?", (course_id,)).fetchone()
            if c_row:
                course = dict(c_row)
                m_rows = cursor.execute("SELECT * FROM course_modules WHERE course_id = ? ORDER BY order_index ASC", (course_id,)).fetchall()
                modules = [dict(m) for m in m_rows]
    except Exception as e:
        print(f"[Courses Detail Error] {e}")

    return templates.TemplateResponse(
        request=request, 
        name="course_detail.html", 
        context={"course": course, "modules": modules}
    )
