import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import IS_SERVERLESS
from app.database import get_db, init_db
from app.routers import pages, questions, papers, vocab, analytics, sources, agents

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")


def seed_if_empty():
    """Populate the database on cold start if it has no starter content.

    Vercel serverless filesystems are ephemeral (SQLite lives in /tmp), so
    every cold start gets a fresh database. seed_data is idempotent and fast,
    and supplies useful fallback content even if OpenSAT is unavailable.
    """
    try:
        with get_db() as conn:
            count = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
        if count == 0:
            from seed_data import seed_all

            seed_all()
    except Exception as e:  # pragma: no cover - never let seeding crash the app
        print(f"[SAT Study Lab] Seed skipped: {e}")


def ingest_opensat_if_empty():
    """Load the full OpenSAT bank once, without making startup fragile.

    The source count makes warm starts and persistent PostgreSQL deployments
    cheap. Set SKIP_OPENSAT_INGEST=1 for offline development or test runs.
    """
    if os.getenv("SKIP_OPENSAT_INGEST", "").lower() in {"1", "true", "yes"}:
        return

    if IS_SERVERLESS and os.getenv("FORCE_OPENSAT_INGEST", "").lower() not in {"1", "true", "yes"}:
        print("[SAT Study Lab] Skipping OpenSAT auto-ingest in serverless environment.")
        return

    try:
        with get_db() as conn:
            count = conn.execute(
                """
                SELECT COUNT(*) FROM questions
                WHERE source_name = 'OpenSAT Community Database'
                """
            ).fetchone()[0]
        if count == 0:
            from scripts.fetch_opensat_data import fetch_and_ingest

            fetch_and_ingest()
    except Exception as e:  # pragma: no cover - remote data must not block app
        print(f"[SAT Study Lab] OpenSAT auto-ingest skipped: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    seed_if_empty()
    ingest_opensat_if_empty()
    yield


app = FastAPI(lifespan=lifespan)

os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon_ico():
    return FileResponse(os.path.join(STATIC_DIR, "favicon.ico"))


@app.get("/favicon.png", include_in_schema=False)
async def favicon_png():
    return FileResponse(os.path.join(STATIC_DIR, "favicon.png"))


app.include_router(pages.router)
app.include_router(questions.router)
app.include_router(papers.router)
app.include_router(vocab.router)
app.include_router(analytics.router)
app.include_router(sources.router)
app.include_router(agents.router)
