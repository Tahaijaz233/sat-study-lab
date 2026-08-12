from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.database import init_db
from app.routers import pages, questions, papers, vocab, analytics, sources, agents
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    os.makedirs("app/static", exist_ok=True)
    os.makedirs("app/templates", exist_ok=True)
    yield

app = FastAPI(lifespan=lifespan)

# Health check endpoint for Fly.io
@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "healthy", "service": "sat-study-lab"})

os.makedirs("app/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages.router)
app.include_router(questions.router)
app.include_router(papers.router)
app.include_router(vocab.router)
app.include_router(analytics.router)
app.include_router(sources.router)
app.include_router(agents.router)
