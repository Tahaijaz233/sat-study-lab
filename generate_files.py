import os

files = {
    "C:/SAT/requirements.txt": """fastapi>=0.115.0
uvicorn[standard]>=0.30.0
jinja2>=3.1.4
pydantic>=2.9.0
pypdf>=5.0.0
python-multipart>=0.0.12
httpx>=0.27.0""",
    "C:/SAT/app/config.py": """import os

class Config:
    DB_PATH = os.getenv("DB_PATH", "sat_lab.db")
    APP_NAME = "SAT Study Lab"

config = Config()
""",
    "C:/SAT/app/database.py": """import sqlite3
from contextlib import contextmanager
from app.config import config

def get_connection():
    conn = sqlite3.connect(config.DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.executescript('''
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY,
            name TEXT,
            license_note TEXT
        );
        CREATE TABLE IF NOT EXISTS passages (
            id INTEGER PRIMARY KEY,
            content TEXT
        );
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            passage_id INTEGER,
            prompt TEXT,
            content_hash TEXT UNIQUE,
            source_id INTEGER,
            FOREIGN KEY (passage_id) REFERENCES passages(id),
            FOREIGN KEY (source_id) REFERENCES sources(id)
        );
        CREATE TABLE IF NOT EXISTS choices (
            id INTEGER PRIMARY KEY,
            question_id INTEGER,
            content TEXT,
            is_correct BOOLEAN,
            FOREIGN KEY (question_id) REFERENCES questions(id)
        );
        CREATE TABLE IF NOT EXISTS question_tags (
            id INTEGER PRIMARY KEY,
            question_id INTEGER,
            tag TEXT,
            FOREIGN KEY (question_id) REFERENCES questions(id)
        );
        CREATE TABLE IF NOT EXISTS vocab_terms (
            id INTEGER PRIMARY KEY,
            term TEXT UNIQUE,
            definition TEXT,
            repetitions INTEGER DEFAULT 0,
            interval REAL DEFAULT 1,
            ef REAL DEFAULT 2.5,
            status TEXT DEFAULT 'forgotten'
        );
        CREATE TABLE IF NOT EXISTS practice_sessions (
            id INTEGER PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed BOOLEAN DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS user_attempts (
            id INTEGER PRIMARY KEY,
            session_id INTEGER,
            question_id INTEGER,
            choice_id INTEGER,
            is_correct BOOLEAN,
            FOREIGN KEY (session_id) REFERENCES practice_sessions(id),
            FOREIGN KEY (question_id) REFERENCES questions(id),
            FOREIGN KEY (choice_id) REFERENCES choices(id)
        );
        
        -- FTS tables
        CREATE VIRTUAL TABLE IF NOT EXISTS questions_fts USING fts5(prompt, content="questions", content_rowid="id");
        CREATE VIRTUAL TABLE IF NOT EXISTS vocab_fts USING fts5(term, definition, content="vocab_terms", content_rowid="id");
        
        -- Sync triggers for questions
        CREATE TRIGGER IF NOT EXISTS questions_ai AFTER INSERT ON questions BEGIN
            INSERT INTO questions_fts(rowid, prompt) VALUES (new.id, new.prompt);
        END;
        CREATE TRIGGER IF NOT EXISTS questions_ad AFTER DELETE ON questions BEGIN
            INSERT INTO questions_fts(questions_fts, rowid, prompt) VALUES('delete', old.id, old.prompt);
        END;
        CREATE TRIGGER IF NOT EXISTS questions_au AFTER UPDATE ON questions BEGIN
            INSERT INTO questions_fts(questions_fts, rowid, prompt) VALUES('delete', old.id, old.prompt);
            INSERT INTO questions_fts(rowid, prompt) VALUES (new.id, new.prompt);
        END;
        
        -- Sync triggers for vocab
        CREATE TRIGGER IF NOT EXISTS vocab_ai AFTER INSERT ON vocab_terms BEGIN
            INSERT INTO vocab_fts(rowid, term, definition) VALUES (new.id, new.term, new.definition);
        END;
        CREATE TRIGGER IF NOT EXISTS vocab_ad AFTER DELETE ON vocab_terms BEGIN
            INSERT INTO vocab_fts(vocab_fts, rowid, term, definition) VALUES('delete', old.id, old.term, old.definition);
        END;
        CREATE TRIGGER IF NOT EXISTS vocab_au AFTER UPDATE ON vocab_terms BEGIN
            INSERT INTO vocab_fts(vocab_fts, rowid, term, definition) VALUES('delete', old.id, old.term, old.definition);
            INSERT INTO vocab_fts(rowid, term, definition) VALUES (new.id, new.term, new.definition);
        END;
        ''')
""",
    "C:/SAT/app/models.py": """from pydantic import BaseModel
from typing import List, Optional

class ChoiceCreate(BaseModel):
    content: str
    is_correct: bool

class QuestionCreate(BaseModel):
    passage_id: Optional[int] = None
    prompt: str
    choices: List[ChoiceCreate]
    tags: List[str] = []

class QuestionResponse(BaseModel):
    id: int
    prompt: str
    passage_id: Optional[int] = None
    content_hash: str

class VocabTermCreate(BaseModel):
    term: str
    definition: str

class SM2Rating(BaseModel):
    q: int

class PracticeSessionCreate(BaseModel):
    num_rw: int = 27
    num_math: int = 22

class AttemptSubmit(BaseModel):
    question_id: int
    choice_id: int

class SourceResponse(BaseModel):
    id: int
    name: str
    license_note: str
""",
    "C:/SAT/app/agents/__init__.py": "",
    "C:/SAT/app/agents/coordinator.py": """class AgentCoordinator:
    def __init__(self):
        pass
    def coordinate(self):
        pass
""",
    "C:/SAT/app/agents/ingestion.py": """import json
from pypdf import PdfReader
import httpx

class IngestionAgent:
    def from_json(self, json_data):
        return json.loads(json_data)
        
    def from_pdf(self, pdf_path):
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
        
    def from_http(self, url):
        return httpx.get(url).text
""",
    "C:/SAT/app/agents/normalization.py": """import hashlib

class NormalizationAgent:
    def compute_hash(self, prompt: str, passage: str = "") -> str:
        return hashlib.sha256((prompt + passage).encode('utf-8')).hexdigest()
""",
    "C:/SAT/app/agents/paper_builder.py": """class PaperBuilderAgent:
    def build_paper(self, db_conn, is_adaptive=False, module1_score=0.0):
        # RW 27 Qs/32m; Math 22 Qs/35m
        paper = {"rw": [], "math": []}
        if is_adaptive:
            difficulty = "hard" if module1_score >= 0.65 else "easy"
            # select based on difficulty
        return paper
""",
    "C:/SAT/app/agents/vocab_agent.py": """class VocabAgent:
    def apply_sm2(self, q: int, repetitions: int, interval: float, ef: float):
        if q >= 3:
            if repetitions == 0:
                interval = 1
            elif repetitions == 1:
                interval = 6
            else:
                interval = interval * ef
            repetitions += 1
            status = 'learned' if q > 3 else 'shaky'
        else:
            repetitions = 0
            interval = 1
            status = 'forgotten'
            
        ef = max(1.3, ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))
        return repetitions, interval, ef, status
""",
    "C:/SAT/app/agents/tutor.py": """class TutorAgent:
    def generate_explanation(self, question, selected_choice):
        return f"Step-by-step reasoning for choice {selected_choice}"
""",
    "C:/SAT/app/agents/qa_compliance.py": """class QAComplianceAgent:
    def audit(self, data):
        issues = []
        if 'prompt' not in data:
            issues.append('Missing prompt')
        if len(data.get('choices', [])) < 2:
            issues.append('Not enough choices')
        return issues
""",
    "C:/SAT/app/agents/analytics_agent.py": """class AnalyticsAgent:
    def calculate_score(self, section, correct, total):
        # scaled SAT score calculation (200-800 per section)
        if total == 0: return 200
        percent = correct / total
        score = 200 + int(percent * 600)
        return min(max(score, 200), 800)
        
    def find_weak_areas(self, attempts):
        # < 70% threshold
        return ["topic"]
""",
    "C:/SAT/app/routers/__init__.py": "",
    "C:/SAT/app/routers/pages.py": """from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
# Just mock it if templates don't exist
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def home(request: Request):
    return {"message": "Home HTML"}

@router.get("/papers")
def papers(request: Request):
    return {"message": "Papers HTML"}

@router.get("/bank")
def bank(request: Request):
    return {"message": "Bank HTML"}

@router.get("/vocab")
def vocab(request: Request):
    return {"message": "Vocab HTML"}

@router.get("/analytics")
def analytics(request: Request):
    return {"message": "Analytics HTML"}

@router.get("/sources")
def sources(request: Request):
    return {"message": "Sources HTML"}
""",
    "C:/SAT/app/routers/questions.py": """from fastapi import APIRouter
router = APIRouter(prefix="/api/questions")

@router.get("/")
def list_questions():
    return []
""",
    "C:/SAT/app/routers/papers.py": """from fastapi import APIRouter
router = APIRouter(prefix="/api/papers")

@router.post("/")
def create_session():
    return {}
""",
    "C:/SAT/app/routers/vocab.py": """from fastapi import APIRouter
router = APIRouter(prefix="/api/vocab")

@router.get("/")
def get_vocab():
    return []
""",
    "C:/SAT/app/routers/analytics.py": """from fastapi import APIRouter
router = APIRouter(prefix="/api/analytics")

@router.get("/")
def get_analytics():
    return {}
""",
    "C:/SAT/app/routers/sources.py": """from fastapi import APIRouter
router = APIRouter(prefix="/api/sources")

@router.get("/")
def get_sources():
    return []
""",
    "C:/SAT/app/routers/agents.py": """from fastapi import APIRouter
router = APIRouter(prefix="/api/agents")

@router.get("/status")
def get_status():
    return {"status": "ok"}
""",
    "C:/SAT/app/main.py": """from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
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

os.makedirs("app/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages.router)
app.include_router(questions.router)
app.include_router(papers.router)
app.include_router(vocab.router)
app.include_router(analytics.router)
app.include_router(sources.router)
app.include_router(agents.router)
""",
    "C:/SAT/run.py": """import os
import subprocess
import sys

def setup():
    try:
        import fastapi
        import uvicorn
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    from app.database import init_db
    init_db()
    # seed_all() Mocked
    
def seed_all():
    pass

if __name__ == "__main__":
    setup()
    seed_all()
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
""",
    "C:/SAT/start.sh": """#!/bin/bash
python3 run.py
"""
}

for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Files created.")
