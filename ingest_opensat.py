import httpx
import json
import uuid
import hashlib
import ast
from datetime import datetime
from app.database import get_db
from app.agents.normalization import NormalizationAgent

OPENSAT_URL = "https://api.jsonsilo.com/public/942c3c3b-3a0c-4be3-81c2-12029def19f5"
normalizer = NormalizationAgent()

def infer_subtopic(domain: str) -> str:
    subtopics_map = {
        "Algebra": "Linear Equations",
        "Advanced Math": "Equivalent Expressions",
        "Problem-Solving and Data Analysis": "Ratios and Rates",
        "Problem Solving and Data Analysis": "Ratios and Rates",
        "Geometry and Trigonometry": "Lines, Angles, and Triangles",
        "Standard English Conventions": "Boundaries and Sentence Structure",
        "Craft and Structure": "Words in Context",
        "Information and Ideas": "Central Ideas and Details",
        "Expression of Ideas": "Transitions"
    }
    return subtopics_map.get(domain, "General SAT Concept")

def fetch_and_ingest():
    print(f"Fetching OpenSAT question database from {OPENSAT_URL}...")
    try:
        response = httpx.get(OPENSAT_URL, timeout=40.0)
        response.raise_for_status()
        raw_data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return {"inserted": 0, "duplicates": 0, "errors": 1}

    stats = {"inserted": 0, "duplicates": 0, "errors": 0}
    
    with get_db() as conn:
        cursor = conn.cursor()

        # Insert source record
        cursor.execute("""
            INSERT OR REPLACE INTO sources (id, name, uri, source_type, permission_notes, imported_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            "opensat_db",
            "OpenSAT Community Database",
            "https://github.com/Anas099X/OpenSAT",
            "api_json",
            "Open source - free to use and modify (MIT)"
        ))

        for section_key in ["math", "english"]:
            section_name = "Math" if section_key == "math" else "Reading & Writing"
            items = raw_data.get(section_key, [])
            
            for item in items:
                try:
                    q_data = item.get("question", {})
                    if isinstance(q_data, str) and q_data.strip().startswith("{"):
                        try:
                            q_data = ast.literal_eval(q_data.strip())
                        except Exception:
                            pass
                    
                    if isinstance(q_data, dict):
                        raw_prompt = str(q_data.get("question", "")).strip()
                        raw_paragraph = str(q_data.get("paragraph", "")).strip()
                    else:
                        raw_prompt = str(q_data).strip()
                        raw_paragraph = ""

                    prompt = normalizer.clean_text(raw_prompt)
                    passage_content = normalizer.clean_passage(raw_paragraph)

                    if not prompt and raw_paragraph:
                        prompt = normalizer.clean_text(raw_paragraph)
                        
                    if not prompt:
                        continue

                    passage_id = None
                    if passage_content:
                        p_hash = hashlib.sha256(passage_content.encode('utf-8')).hexdigest()[:16]
                        
                        # Check existing passage
                        existing_p = cursor.execute("SELECT id FROM passages WHERE id = ?", (p_hash,)).fetchone()
                        if existing_p:
                            passage_id = existing_p[0]
                        else:
                            passage_id = p_hash
                            cursor.execute("""
                                INSERT INTO passages (id, title, content, passage_type, word_count, source_name, source_uri, content_hash)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                passage_id,
                                f"OpenSAT Passage - {item.get('domain', 'General')}",
                                passage_content,
                                f"{section_name} Passage",
                                len(passage_content.split()),
                                "OpenSAT Community Database",
                                "https://github.com/Anas099X/OpenSAT",
                                p_hash
                            ))

                    content_hash = normalizer.compute_hash(prompt, passage_content)

                    # Check duplicate question
                    existing_q = cursor.execute("SELECT id FROM questions WHERE content_hash = ?", (content_hash,)).fetchone()
                    if existing_q:
                        stats["duplicates"] += 1
                        continue

                    question_id = str(uuid.uuid4())
                    domain = item.get("domain", "General SAT Concept")
                    subtopic = infer_subtopic(domain)
                    difficulty = str(item.get("difficulty") or "Medium").strip().capitalize()
                    if difficulty not in ["Easy", "Medium", "Hard"]:
                        difficulty = "Medium"

                    choices_dict = q_data.get("choices", {}) if isinstance(q_data, dict) else {}
                    question_type = "Multiple Choice" if choices_dict else "Student-Produced Response"
                    correct_answer = normalizer.clean_text(q_data.get("correct_answer", "") if isinstance(q_data, dict) else "")
                    explanation = normalizer.clean_text(q_data.get("explanation", "Detailed explanation provided by OpenSAT community.") if isinstance(q_data, dict) else "")

                    cursor.execute("""
                        INSERT INTO questions (
                            id, passage_id, section, topic, subtopic, question_type,
                            difficulty, prompt, answer_explanation, correct_answer_value,
                            source_name, source_uri, import_status, license_notes, content_hash
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        question_id, passage_id, section_name, domain, subtopic, question_type,
                        difficulty, prompt, explanation, correct_answer,
                        "OpenSAT Community Database", "https://github.com/Anas099X/OpenSAT",
                        "active", "Open source (MIT)", content_hash
                    ))

                    # Insert choices
                    if choices_dict and isinstance(choices_dict, dict):
                        for letter, content in choices_dict.items():
                            clean_content = normalizer.clean_text(content)
                            is_correct = 1 if letter.strip().upper() == correct_answer.strip().upper() or clean_content.strip().upper() == correct_answer.strip().upper() else 0
                            choice_id = str(uuid.uuid4())
                            cursor.execute("""
                                INSERT INTO choices (id, question_id, choice_letter, content, is_correct)
                                VALUES (?, ?, ?, ?, ?)
                            """, (choice_id, question_id, letter.strip().upper(), clean_content, is_correct))

                    stats["inserted"] += 1

                except Exception as ex:
                    stats["errors"] += 1
                    print(f"Item error: {ex}")

        # Update source count
        cursor.execute("""
            UPDATE sources 
            SET question_count = (SELECT COUNT(*) FROM questions WHERE source_name = 'OpenSAT Community Database')
            WHERE id = 'opensat_db'
        """)

    print(f"Ingestion Finished! Inserted: {stats['inserted']}, Duplicates skipped: {stats['duplicates']}, Errors: {stats['errors']}")
    return stats

if __name__ == "__main__":
    fetch_and_ingest()
