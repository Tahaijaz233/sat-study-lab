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
│   ├── config.py          # App configurations
│   ├── database.py        # SQLite connection manager & FTS5 schema init
│   └── main.py            # FastAPI main app instance
├── ingest_opensat.py      # OpenSAT API dataset fetcher & parser
├── seed_courses.py        # Course content curriculum seeder
├── seed_data.py           # Core vocabulary & initial question seeder
├── run.py                 # Startup script & Uvicorn dev server
├── run_tests.py           # Test runner for unittest suite
├── requirements.txt       # Python dependencies
└── README.md              # Documentation
```

---

## 🌐 Deployment Guidelines

### Fly.io + Neon PostgreSQL (Recommended for Production)

This is the recommended deployment stack for production use:

- **Fly.io**: Hosts the FastAPI application as a long-running VM
- **Neon PostgreSQL**: Hosted serverless PostgreSQL database (free tier, no expiration)

#### Prerequisites
1. Install Fly.io CLI:
   ```bash
   curl -L https://fly.io/install | sh
   ```
2. Log in to Fly.io:
   ```bash
   fly auth login
   ```

#### Step 1: Set Database Secret
Your Neon PostgreSQL connection string needs to be set as a Fly.io secret:
```bash
fly secrets set DATABASE_URL="postgresql://neondb_owner:[npg_YwTGSXL8O0Jt@ep-wispy-bar-azpy15r9-pooler.c-3.ap-southeast-1.aws.neon.tech]/neondb?sslmode=require&channel_binding=require"
```

#### Step 2: Deploy to Fly.io
```bash
# Initialize the app (if not already done)
fly launch --name sat-study-lab --region sin --no-deploy

# Deploy the application
fly deploy
```

#### Step 3: Verify Deployment
```bash
# Check app status
fly status

# View live logs
fly logs

# Open the app in your browser
fly open
```

Your app will be available at `https://sat-study-lab.sin.fly.dev` (or whatever URL Fly.io assigns).

---

### Local Development (SQLite)

For local development, the app uses SQLite by default. No `DATABASE_URL` environment variable is needed.

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py

# Access at http://localhost:8000
```

---

### Other Platforms

- **Railway**: Works with either SQLite (with persistent volume) or Neon PostgreSQL
- **Vercel / AWS Lambda**: Serverless platforms use ephemeral file systems. If deploying to Vercel, you MUST use Neon PostgreSQL (set `DATABASE_URL` env var) — SQLite will not persist.

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).
