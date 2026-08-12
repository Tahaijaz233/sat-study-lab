from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, Response
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

# Health check endpoint for monitoring
@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "healthy", "service": "sat-study-lab"})

# Favicon endpoint - returns a simple SVG favicon to prevent 404 errors
@app.get("/favicon.ico")
@app.get("/favicon.png")
async def favicon():
    """Return a simple favicon to prevent browser 404 errors."""
    svg_favicon = b"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="15" fill="#1e40af"/>
  <text x="50" y="68" font-size="50" text-anchor="middle" fill="white" font-family="Arial" font-weight="bold">S</text>
</svg>"""
    return Response(content=svg_favicon, media_type="image/svg+xml")

os.makedirs("app/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages.router)
app.include_router(questions.router)
app.include_router(papers.router)
app.include_router(vocab.router)
app.include_router(analytics.router)
app.include_router(sources.router)
app.include_router(agents.router)
