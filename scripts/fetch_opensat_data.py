import httpx
import sqlite3
import json
import sys
from pathlib import Path

# Add project root to path so we can import app modules
sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.database import get_db
from app.agents.normalization import NormalizationAgent

# Create a normalization agent instance
normalizer = NormalizationAgent()

def fetch_and_ingest():
    print("Fetching OpenSAT questions from Pinesat API...")
    url = "https://pinesat.duckdns.org/api/questions"
    
    try:
        response = httpx.get(url, timeout=30.0)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    # Check if data has a 'data' field or is just a list
    questions = data.get('data', []) if isinstance(data, dict) else data
    if not isinstance(questions, list):
        print("Unexpected JSON structure.")
        return

    print(f"Fetched {len(questions)} questions. Normalizing and inserting into database...")
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Ensure openSAT source exists
        source_id = "src_opensat"
        cursor.execute("""
            INSERT OR IGNORE INTO sources (id, name, uri, source_type, permission_notes, question_count)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (source_id, "OpenSAT", "https://github.com/Anas099X/OpenSAT", "api", "MIT License", 0))

        added_count = 0
        for q in questions:
            # PINESAT API format usually looks like:
            # { "id": ..., "passage": "...", "question": "...", "options": ["A", "B", "C", "D"], "correct_answer": "...", "explanation": "...", "section": "...", "domain": "..." }
            
            prompt = str(q.get('question') or q.get('prompt') or "")
            passage_text = str(q.get('passage') or '')
            section = q.get('section', 'Reading & Writing')
            topic = q.get('domain', 'Information and Ideas')
            subtopic = q.get('skill', topic)
            options = q.get('options') or q.get('choices') or []
            correct_val = q.get('correct_answer') or q.get('correct') or ""
            explanation = q.get('explanation') or q.get('rationale') or ""
            
            if not prompt:
                continue
                
            q_type = "Multiple Choice" if options else "Student-Produced Response"
            
            passage_id = None
            if passage_text:
                # Calculate a hash for the passage to reuse if exists
                p_hash = normalizer.compute_hash(passage_text)
                cursor.execute("SELECT id FROM passages WHERE content_hash = ?", (p_hash,))
                p_row = cursor.fetchone()
                if p_row:
                    passage_id = p_row['id']
                else:
                    import uuid
                    passage_id = f"p_{uuid.uuid4().hex[:12]}"
                    cursor.execute("""
                        INSERT INTO passages (id, title, content, content_hash)
                        VALUES (?, ?, ?, ?)
                    """, (passage_id, "OpenSAT Passage", passage_text, p_hash))
                    
            # Normalize prompt + passage for unique hash
            content_hash = normalizer.compute_hash(prompt, passage_text)
            
            # Check if exists
            cursor.execute("SELECT id FROM questions WHERE content_hash = ?", (content_hash,))
            if cursor.fetchone():
                continue
                
            import uuid
            new_q_id = f"q_{uuid.uuid4().hex[:12]}"
            
            # Insert question
            cursor.execute("""
                INSERT INTO questions (id, prompt, passage_id, section, topic, subtopic, difficulty, correct_answer_value, answer_explanation, source_name, source_uri, license_notes, question_type, content_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                new_q_id,
                prompt,
                passage_id,
                section.title() if "math" not in section.lower() else "Math",
                topic,
                subtopic,
                "medium", # default difficulty
                str(correct_val).strip() if q_type == "Student-Produced Response" else None,
                explanation,
                "OpenSAT",
                "https://github.com/Anas099X/OpenSAT",
                "MIT License",
                q_type,
                content_hash
            ))
            
            # Insert choices if Multiple Choice
            if q_type == "Multiple Choice":
                # Some APIs provide options as ["Apples", "Oranges", "Bananas", "Pears"] and correct_answer as "A" or "Apples".
                # We need to map them to ChoiceCreate format.
                letters = ["A", "B", "C", "D", "E"]
                for i, opt in enumerate(options):
                    letter = letters[i] if i < len(letters) else "?"
                    is_correct = (str(correct_val).strip().upper() == letter) or (str(correct_val).strip() == str(opt).strip())
                    
                    choice_id = f"c_{uuid.uuid4().hex[:12]}"
                    cursor.execute("""
                        INSERT INTO choices (id, question_id, choice_letter, content, is_correct)
                        VALUES (?, ?, ?, ?, ?)
                    """, (choice_id, new_q_id, letter, str(opt), 1 if is_correct else 0))
            
            added_count += 1
            
        # Update source question count
        cursor.execute("UPDATE sources SET question_count = (SELECT count(*) FROM questions WHERE source_name = ?) WHERE id = ?", ("OpenSAT", source_id))
        print(f"Successfully added {added_count} new questions from OpenSAT.")

if __name__ == "__main__":
    fetch_and_ingest()
