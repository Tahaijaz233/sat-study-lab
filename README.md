# 🎓 Digital SAT Study Lab

A modern, full-stack, automated test-prep and practice platform built specifically for the **Digital SAT (DSAT)**. 

Featuring official College Board domain quota distributions, dynamic adaptive module routing, full-text search question banks, interactive vocabulary flashcards powered by the **SuperMemo SM-2 spaced repetition algorithm**, and integrated course content.

---

## ✨ Features

- 📝 **Adaptive Practice Test Engine**:
  - Simulates the official Digital SAT test layout with split-pane passage viewing, question navigation, timer, and question bookmarking.
  - **Dynamic Adaptive Routing**: Module 1 performance determines Module 2 difficulty routing (Score $\ge 65\%$ routes to the **Hard** adaptive path; $< 65\%$ routes to **Easy**).
  - Exact domain and skill quotas for both **Reading & Writing** (27 questions/module) and **Math** (22 questions/module).
  
- 📚 **Searchable Question Bank**:
  - Instant full-text search powered by **SQLite FTS5**.
  - Filter by section (Reading & Writing vs. Math), difficulty (Easy, Medium, Hard), or domain tags.
  - Ingestion pipeline supporting OpenSAT API and custom PDF uploading.

- 🎴 **Vocab Center with Spaced Repetition (SM-2)**:
  - Interactive 3D flip-card vocabulary trainer.
  - Implements the **SuperMemo SM-2** spaced repetition algorithm with dynamic Easiness Factor (EF) bounds ($EF \ge 1.3$).
  - Tracks review intervals and categorizes terms into `unseen`, `learning`, `shaky`, and `learned`.

- 📖 **Interactive Course Modules**:
  - Comprehensive Digital SAT Math and Reading & Writing study courses.
  - Expandable accordion lessons rendered dynamically with Markdown, syntax highlighting, and live **KaTeX** math formulas.
  - Targeted drill launcher directly from course topics.

- 📊 **Performance Analytics**:
  - Detailed score breakdown, accuracy percentages, time spent per question, and skill-level diagnostic reports.

---

## 🛠️ Tech Stack & Architecture

- **Backend**: Python 3.10+, FastAPI, Uvicorn
- **Database**: SQLite3 by default; persistent PostgreSQL when `DATABASE_URL` is configured
- **Frontend**: HTML5, Vanilla CSS, TailwindCSS, JavaScript (ES6+)
- **Libraries**: KaTeX (Math rendering), Marked.js (Markdown parsing), Lucide (Icons), PyPDF (PDF ingestion)
- **Testing**: Python `unittest` test suite

---

## 🚀 Installation & Local Setup

### Prerequisites
- **Python 3.10** or higher installed on your system.
- **Git** installed.

### Step 1: Clone the Repository
```bash
git clone https://github.com/Tahaijaz233/sat-study-lab.git
cd sat-study-lab
```

### Step 2: Create a Virtual Environment (Optional but Recommended)
```bash
# On macOS / Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize & Seed the Database
Run the setup script to automatically initialize the SQLite database schema and populate seed data:
```bash
python run.py
```
The complete OpenSAT English and Math question bank is ingested automatically
on the first application startup. The import is idempotent; to run it manually:
```bash
python scripts/fetch_opensat_data.py
```

SQLite is used when no database environment variable is configured. For a
persistent PostgreSQL deployment, set:
```bash
export DATABASE_URL="postgresql://user:password@host:5432/database"
```

---

## 💻 Running the Application

Start the local server using `run.py`:
```bash
python run.py
```
Once started, open your browser and navigate to:
👉 **[http://localhost:8000](http://localhost:8000)**

---

## ▲ Deploying to Vercel

The app runs on Vercel as a single Python serverless function (FastAPI's ASGI
support is built into Vercel's Python runtime — no adapter needed).

```bash
# 1. Install the Vercel CLI
npm i -g vercel

# 2. From the repo root, log in and link/deploy
vercel login
vercel
```

Or connect the GitHub repository from the [Vercel dashboard](https://vercel.com)
— Vercel auto-detects the FastAPI app in `app/main.py`.

What's already configured:

- **`api/index.py`** — explicit Vercel entrypoint shim (re-exports the FastAPI
  `app` from `app/main.py`).
- **`vercel.json`** — bumps the function `maxDuration` to 60s for cold starts.
- **Persistent PostgreSQL support** — set `DATABASE_URL` to a hosted Postgres
  database (such as Neon). Without it, `app/config.py` falls back to SQLite and
  uses `/tmp/sat_lab.db` on Vercel's read-only serverless filesystem.
- **Automatic OpenSAT import** — the complete English and Math bank is fetched
  from the public OpenSAT API on first startup, with hash-based deduplication.
- **Favicon** — `app/static/favicon.ico` + `favicon.png` served at `/favicon.ico`
  and `/favicon.png`, with `<link rel="icon">` tags in `app/templates/base.html`.

> ⚠️ **Note:** Vercel function storage is ephemeral when `DATABASE_URL` is not
> configured, so SQLite-backed sessions and progress reset on cold starts. Use
> a hosted PostgreSQL database for persistence.

---

## 🧪 Running Automated Tests

To execute the full automated test suite (verifying SM-2 calculations, adaptive module quotas, database FTS5 queries, and API endpoints):

```bash
python run_tests.py
```

All 43 automated unit and integration tests should pass with an `OK` status.

---

## 📂 Project Structure

```
SAT-Study-Lab/
├── app/
│   ├── agents/            # Multi-agent system (PaperBuilder, Ingestion, Vocab, etc.)
│   ├── routers/           # FastAPI API endpoints (questions, papers, vocab, analytics)
│   ├── static/            # Frontend CSS styles, JS modules, assets, favicon
│   ├── templates/         # Jinja2 HTML views (papers, question bank, courses, vocab)
│   ├── config.py          # App configurations
│   ├── database.py        # SQLite/PostgreSQL connection manager and schemas
│   └── main.py            # FastAPI main app instance
├── api/
│   └── index.py           # Vercel serverless entrypoint (FastAPI shim)
├── ingest_opensat.py      # OpenSAT API dataset fetcher & parser
├── seed_courses.py        # Course content curriculum seeder
├── seed_data.py           # Core vocabulary & initial question seeder
├── run.py                 # Startup script & Uvicorn dev server
├── run_tests.py           # Test runner for unittest suite
├── requirements.txt       # Python dependencies
├── vercel.json            # Vercel function configuration
└── README.md              # Documentation
```

## 📄 License

This project is open-source under the [MIT License](LICENSE).
