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
- **Database**: SQLite3 with WAL (Write-Ahead Logging) mode, Foreign Keys, and FTS5 Virtual Tables
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
*(Optional)* To pull the full 1,500+ question dataset directly from OpenSAT, run the ingestion script:
```bash
python ingest_opensat.py
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

## 🧪 Running Automated Tests

To execute the full automated test suite (verifying SM-2 calculations, adaptive module quotas, database FTS5 queries, and API endpoints):

```bash
python run_tests.py
```

All 18 automated unit and integration tests should pass with an `OK` status.

---

## 📂 Project Structure

```
SAT-Study-Lab/
├── app/
│   ├── agents/            # Multi-agent system (PaperBuilder, Ingestion, Vocab, etc.)
│   ├── routers/           # FastAPI API endpoints (questions, papers, vocab, analytics)
│   ├── static/            # Frontend CSS styles, JS modules, assets
│   ├── templates/         # Jinja2 HTML views (papers, question bank, courses, vocab)
│   ├── config.py          # App configurations (reads DATABASE_URL env var if set)
│   ├── database.py        # Database connection manager (SQLite or PostgreSQL)
│   └── main.py            # FastAPI main app instance
├── api/
│   └── index.py           # Vercel serverless handler (Mangum wrapper for FastAPI)
├── ingest_opensat.py      # OpenSAT API dataset fetcher & parser
├── seed_courses.py        # Course content curriculum seeder
├── seed_data.py           # Core vocabulary & initial question seeder
├── run.py                 # Startup script & Uvicorn dev server
├── run_tests.py           # Test runner for unittest suite
├── requirements.txt       # Python dependencies
├── vercel.json            # Vercel deployment configuration (optional)
└── README.md              # Documentation
```

**Key Files for Local Use:**
- `run.py` — Start the app locally
- `requirements.txt` — Install dependencies
- `app/config.py` — Set `DATABASE_URL` env var for PostgreSQL (optional, defaults to SQLite)

---

## 🌐 Deployment Guidelines

### Running Locally (Default & Recommended for Personal Use)

This project is designed to run locally on your own computer using **SQLite**. This is the simplest and most common way to use SAT Study Lab:

```bash
# Clone and enter the repository
git clone https://github.com/Tahaijaz233/sat-study-lab.git
cd sat-study-lab

# Install dependencies
pip install -r requirements.txt

# Run the application (creates SQLite database automatically)
python run.py

# Open your browser to http://localhost:8000
```

Your data is stored in `sat_lab.db` (SQLite) in the project directory. You have full control over your data.

---

### Other Deployment Options

- **Railway**: Supports both SQLite (with persistent volume) and PostgreSQL
- **Fly.io**: Long-running VM with PostgreSQL
- **Any Python host**: Works with PostgreSQL by setting the `DATABASE_URL` environment variable

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).
