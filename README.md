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

### Vercel + Neon PostgreSQL (Recommended for Production)

This is the recommended deployment stack for production use:

- **Vercel**: Hosts the FastAPI application as serverless functions (auto-scaling, no server management)
- **Neon PostgreSQL**: Hosted serverless PostgreSQL database (free tier, no expiration, connection pooling built-in)

#### ⚠️ Important Vercel Constraints
- **10 second timeout** on Hobby (free) tier — practice test generation may take longer
- Consider upgrading to Vercel Pro if you hit timeout limits
- Use Neon's connection pooler (included in your connection string)

---

#### Prerequisites
1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```
2. Log in to Vercel:
   ```bash
   vercel login
   ```

#### Step 1: Add Neon PostgreSQL as Environment Variable

Your Neon connection string must be added as a Vercel environment variable:

**Via Vercel Dashboard:**
1. Go to your project on [vercel.com](https://vercel.com)
2. Navigate to **Settings → Environment Variables**
3. Add a new variable:
   - **Key**: `DATABASE_URL`
   - **Value**: `postgresql://neondb_owner:npg_YwTGSXL8O0Jt@ep-wispy-bar-azpy15r9-pooler.c-3.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require`
   - **Environment**: Production, Preview, Development (check all that apply)

**Via Vercel CLI:**
```bash
vercel env add DATABASE_URL
# Paste your Neon connection string when prompted
vercel env pull .env.local  # Download to local for testing
```

> **Note:** Your connection string uses Neon's built-in connection pooler (`ep-...-pooler`). This is essential for serverless deployments where each function invocation creates a new connection.

#### Step 2: Deploy to Vercel

**Option A: Via Vercel Dashboard (Easiest)**
1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository: `Tahaijaz233/sat-study-lab`
3. Vercel will auto-detect the configuration
4. Add the `DATABASE_URL` environment variable in settings
5. Click **Deploy**

**Option B: Via Vercel CLI**
```bash
# Link the project
vercel

# Deploy to production
vercel --prod
```

#### Step 3: Verify Deployment

```bash
# Check deployment status
vercel status

# View logs (real-time)
vercel logs

# Open the app in your browser
vercel open
```

Your app will be available at `https://sat-study-lab.vercel.app` (or your custom domain).

---

#### Architecture: How It Works on Vercel

```
┌─────────────────────────────────────────────────────────────┐
│                     Vercel Serverless                        │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  api/index.py (Mangum Handler)                          ││
│  │  ┌─────────────────────────────────────────────────────┐││
│  │  │  FastAPI App (app/main.py)                         │││
│  │  │  - All routers included                            │││
│  │  │  - Jinja2 templates rendered                        │││
│  │  └─────────────────────────────────────────────────────┘││
│  │  Creates DB connection per request                      ││
│  └─────────────────────────────────────────────────────────┘│
│                           │                                  │
│                           ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  Neon PostgreSQL (Connection Pooler)                   ││
│  │  - Handles connection pooling                           ││
│  │  - Scales automatically                                 ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

**Per-Request Flow:**
1. User makes HTTP request → Vercel routes to `api/index.py`
2. Mangum handler invokes FastAPI app
3. App creates a fresh PostgreSQL connection (via Neon pooler)
4. Request is processed, response returned
5. Connection closed (Neon pooler manages actual connections)

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

To test with PostgreSQL locally (matching production):

```bash
# Set the DATABASE_URL environment variable
export DATABASE_URL="postgresql://user:password@localhost:5432/dbname"

# Run the application
python run.py
```

---

### Project Structure (Updated for Vercel)

```
SAT-Study-Lab/
├── app/
│   ├── agents/            # Multi-agent system (PaperBuilder, Ingestion, Vocab, etc.)
│   ├── routers/           # FastAPI API endpoints (questions, papers, vocab, analytics)
│   ├── static/            # Frontend CSS styles, JS modules, assets
│   ├── templates/         # Jinja2 HTML views (papers, question bank, courses, vocab)
│   ├── config.py          # App configurations (DATABASE_URL env var)
│   ├── database.py        # PostgreSQL/SQLite connection manager
│   └── main.py            # FastAPI main app instance
├── api/
│   └── index.py           # Vercel serverless handler (Mangum wrapper)
├── ingest_opensat.py      # OpenSAT API dataset fetcher & parser
├── seed_courses.py        # Course content curriculum seeder
├── seed_data.py           # Core vocabulary & initial question seeder
├── run.py                 # Startup script & Uvicorn dev server
├── run_tests.py           # Test runner for unittest suite
├── requirements.txt       # Python dependencies (includes mangum, psycopg2-binary)
├── vercel.json            # Vercel deployment configuration
└── README.md              # Documentation
```

---

### Troubleshooting Vercel Deployment

**Issue: "Connection timeout" errors**
- Ensure your Neon connection string is correct
- Verify the pooler endpoint is being used (should contain `pooler` in the hostname)
- Cold starts may take 1-2 seconds on first invocation

**Issue: Function timeout (10s limit)**
- Practice test generation queries multiple questions — may exceed 10s
- Solutions:
  1. Upgrade to Vercel Pro (60s timeout)
  2. Optimize queries (add database indexes)
  3. Split large operations into multiple requests

**Issue: "Module not found" errors**
- Ensure `requirements.txt` is at the project root
- Verify all imports use relative paths correctly
- Check that `api/index.py` has correct `sys.path` configuration

**Issue: Database schema not initialized**
- The `init_db()` function runs on app startup via lifespan
- On Vercel, this runs on each cold start
- If tables don't exist, check Vercel logs for schema creation errors

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).
