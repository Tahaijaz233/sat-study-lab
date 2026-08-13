import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

NEON_DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
if not NEON_DATABASE_URL:
    print("Error: DATABASE_URL environment variable is not set. Please provide DATABASE_URL.")
    sys.exit(1)

from app.config import config
config.DATABASE_URL = NEON_DATABASE_URL

from app.database import get_db, init_db, is_postgres
from seed_data import seed_all
import scripts.seed_rw_courses as seed_rw
import scripts.seed_math_courses as seed_math
import scripts.seed_expanded_vocab as seed_vocab
from scripts.fetch_opensat_data import fetch_and_ingest

def main():
    print(f"Targeting Neon PostgreSQL (is_postgres={is_postgres()})...")
    
    # 1. Initialize DB and Schema & Run Data Repairs
    print("\n--- 1. Initializing DB Schema in Neon PostgreSQL ---")
    init_db()
    print("Schema initialized successfully.")
    
    # 2. Seed starter data
    print("\n--- 2. Seeding Core Starter Data ---")
    seed_all()
    
    # 3. Seed Courses
    print("\n--- 3. Seeding Courses (RW + Math) ---")
    try:
        seed_rw.seed_database()
    except Exception as e:
        print(f"RW Courses seed error: {e}")
        
    try:
        seed_math.seed_courses()
    except Exception as e:
        print(f"Math Courses seed error: {e}")
        
    # 4. Seed Expanded Vocab
    print("\n--- 4. Seeding Expanded Vocab ---")
    try:
        seed_vocab.seed_database()
    except Exception as e:
        print(f"Expanded vocab seed error: {e}")
        
    # 5. Ingest Clean OpenSAT Questions
    print("\n--- 5. Ingesting Clean OpenSAT Questions ---")
    stats = fetch_and_ingest()
    print("OpenSAT Ingestion Stats:", stats)
    
    # 6. Verify Database Contents
    print("\n--- 6. Verifying Neon PostgreSQL Counts ---")
    with get_db() as conn:
        cursor = conn.cursor()
        q_count = cursor.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
        p_count = cursor.execute("SELECT COUNT(*) FROM passages").fetchone()[0]
        c_count = cursor.execute("SELECT COUNT(*) FROM choices").fetchone()[0]
        v_count = cursor.execute("SELECT COUNT(*) FROM vocab_terms").fetchone()[0]
        crs_count = cursor.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
        mod_count = cursor.execute("SELECT COUNT(*) FROM course_modules").fetchone()[0]
        src_count = cursor.execute("SELECT COUNT(*) FROM sources").fetchone()[0]
        
        # Check sample passage and prompt
        sample = cursor.execute("""
            SELECT q.prompt, p.content 
            FROM questions q 
            JOIN passages p ON q.passage_id = p.id 
            WHERE q.source_name = 'OpenSAT Community Database' 
            LIMIT 1
        """).fetchone()
        
    print(f"Questions:     {q_count}")
    print(f"Passages:      {p_count}")
    print(f"Choices:       {c_count}")
    print(f"Vocab Terms:   {v_count}")
    print(f"Courses:       {crs_count}")
    print(f"Modules:       {mod_count}")
    print(f"Sources:       {src_count}")
    
    if sample:
        print("\n--- Sample OpenSAT Item in Neon Postgres ---")
        prompt_text = sample[0] if isinstance(sample, (tuple, list)) else sample['prompt']
        passage_text = sample[1] if isinstance(sample, (tuple, list)) else sample['content']
        print("Prompt: ", prompt_text)
        print("Passage:", passage_text)

if __name__ == "__main__":
    main()
