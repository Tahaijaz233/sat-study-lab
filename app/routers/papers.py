import uuid
import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.database import get_db
from app.agents.paper_builder import PaperBuilderAgent

router = APIRouter(prefix="/api/papers", tags=["Papers"])
paper_builder = PaperBuilderAgent()

class SessionCreateRequest(BaseModel):
    title: str
    section: str # "Reading & Writing", "Math", "Full Test"
    session_type: str = "practice"

class AnswerSubmitRequest(BaseModel):
    question_id: str
    selected_choice_id: Optional[str] = None
    student_produced_answer: Optional[str] = None
    time_spent_seconds: int = 0
    bookmarked: bool = False

class DrillRequest(BaseModel):
    topic: str
    subtopic: str
    section: str
    num_questions: int = 10

@router.post("/sessions")
async def create_practice_session(req: SessionCreateRequest):
    session_id = f"sess_{uuid.uuid4().hex[:10]}"
    
    if req.section == "Reading & Writing":
        total_q = 54
    elif req.section == "Math":
        total_q = 44
    else:
        total_q = 98 # Full Test
        
    time_limit = total_q * 90
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO practice_sessions (id, title, section, session_type, total_questions, time_limit_seconds, status)
            VALUES (?, ?, ?, ?, ?, ?, 'in_progress')
        """, (session_id, req.title, req.section, req.session_type, total_q, time_limit))
        
    return {
        "session_id": session_id,
        "title": req.title,
        "section": req.section,
        "total_questions": total_q
    }


def fetch_detailed_questions(cursor, q_ids):
    detailed = []
    for qid in q_ids:
        # Explicitly select only the fields safe to expose to students
        # Exclude answer_explanation and correct_answer_value
        row = cursor.execute("""
            SELECT 
                q.id, q.passage_id, q.section, q.topic, q.subtopic,
                q.question_type, q.difficulty, q.prompt, q.source_name,
                q.source_uri, q.import_status, q.license_notes, q.content_hash,
                q.created_at,
                p.title as passage_title, p.content as passage_content
            FROM questions q
            LEFT JOIN passages p ON q.passage_id = p.id
            WHERE q.id = ?
        """, (qid,)).fetchone()
        if row:
            q_dict = dict(row)
            choices = cursor.execute("SELECT id, choice_letter, content FROM choices WHERE question_id = ? ORDER BY choice_letter", (qid,)).fetchall()
            q_dict['choices'] = [{"id": c["id"], "choice_letter": c["choice_letter"], "content": c["content"]} for c in choices]
            detailed.append(q_dict)
    return detailed

@router.post("/sessions/{session_id}/next_module")
async def next_module(session_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        
        session_row = cursor.execute("SELECT * FROM practice_sessions WHERE id = ?", (session_id,)).fetchone()
        if not session_row:
            raise HTTPException(status_code=404, detail="Session not found")
            
        if session_row['status'] == 'completed':
            return {"completed": True, "score_scaled": session_row['score_scaled']}
            
        # Get all attempts
        attempts = cursor.execute("""
            SELECT a.*, q.section
            FROM user_attempts a
            JOIN questions q ON a.question_id = q.id
            WHERE a.session_id = ?
            ORDER BY a.created_at ASC
        """, (session_id,)).fetchall()
        
        rw_attempts = [a for a in attempts if a['section'] == 'Reading & Writing']
        math_attempts = [a for a in attempts if a['section'] == 'Math']
        
        # Determine current stage based on attempt counts
        num_rw = len(rw_attempts)
        num_math = len(math_attempts)
        
        q_ids = []
        module_name = ""
        time_limit = 0
        
        all_attempted_ids = [a['question_id'] for a in attempts]
        
        if session_row['section'] == 'Reading & Writing':
            if num_rw == 0:
                module_name = "Reading & Writing - Module 1"
                time_limit = 32 * 60
                q_ids = paper_builder.build_module(cursor, "Reading & Writing", "baseline", 27, all_attempted_ids)
            elif num_rw == 27:
                acc = paper_builder.calculate_accuracy(cursor, session_id, [a['question_id'] for a in rw_attempts[:27]])
                diff = "hard" if acc >= 0.65 else "easy"
                module_name = f"Reading & Writing - Module 2 ({diff.title()})"
                time_limit = 32 * 60
                q_ids = paper_builder.build_module(cursor, "Reading & Writing", diff, 27, all_attempted_ids)
            else:
                return await complete_session_internal(cursor, session_id, session_row)
                
        elif session_row['section'] == 'Math':
            if num_math == 0:
                module_name = "Math - Module 1"
                time_limit = 35 * 60
                q_ids = paper_builder.build_module(cursor, "Math", "baseline", 22, all_attempted_ids)
            elif num_math == 22:
                acc = paper_builder.calculate_accuracy(cursor, session_id, [a['question_id'] for a in math_attempts[:22]])
                diff = "hard" if acc >= 0.65 else "easy"
                module_name = f"Math - Module 2 ({diff.title()})"
                time_limit = 35 * 60
                q_ids = paper_builder.build_module(cursor, "Math", diff, 22, all_attempted_ids)
            else:
                return await complete_session_internal(cursor, session_id, session_row)
                
        elif session_row['section'] == 'Full Test':
            if num_rw == 0:
                module_name = "Reading & Writing - Module 1"
                time_limit = 32 * 60
                q_ids = paper_builder.build_module(cursor, "Reading & Writing", "baseline", 27, all_attempted_ids)
            elif num_rw == 27:
                acc = paper_builder.calculate_accuracy(cursor, session_id, [a['question_id'] for a in rw_attempts[:27]])
                diff = "hard" if acc >= 0.65 else "easy"
                module_name = f"Reading & Writing - Module 2 ({diff.title()})"
                time_limit = 32 * 60
                q_ids = paper_builder.build_module(cursor, "Reading & Writing", diff, 27, all_attempted_ids)
            elif num_rw == 54 and num_math == 0:
                module_name = "Math - Module 1"
                time_limit = 35 * 60
                q_ids = paper_builder.build_module(cursor, "Math", "baseline", 22, all_attempted_ids)
            elif num_rw == 54 and num_math == 22:
                acc = paper_builder.calculate_accuracy(cursor, session_id, [a['question_id'] for a in math_attempts[:22]])
                diff = "hard" if acc >= 0.65 else "easy"
                module_name = f"Math - Module 2 ({diff.title()})"
                time_limit = 35 * 60
                q_ids = paper_builder.build_module(cursor, "Math", diff, 22, all_attempted_ids)
            else:
                return await complete_session_internal(cursor, session_id, session_row)
        
        if session_row['session_type'].startswith('drill|'):
            if len(attempts) > 0:
                # Drill only has 1 module, so if there are attempts, it means they submitted the module and we complete it
                return await complete_session_internal(cursor, session_id, session_row)
            
            _, topic, subtopic = session_row['session_type'].split('|')
            limit = session_row['total_questions']
            module_name = f"Drill: {subtopic}"
            time_limit = limit * 90
            
            # Fetch random questions matching topic/subtopic
            rows = cursor.execute("SELECT id FROM questions WHERE topic = ? AND subtopic = ? ORDER BY RANDOM() LIMIT ?", (topic, subtopic, limit)).fetchall()
            q_ids = [r['id'] for r in rows]
            
            # If no questions found, complete immediately to avoid error
            if not q_ids:
                return await complete_session_internal(cursor, session_id, session_row)
                
        detailed_questions = fetch_detailed_questions(cursor, q_ids)
        
        return {
            "completed": False,
            "module_name": module_name,
            "time_limit_seconds": time_limit,
            "questions": detailed_questions
        }

async def complete_session_internal(cursor, session_id, session_row):
    completed_at = datetime.datetime.now().isoformat()
    attempts = cursor.execute("SELECT is_correct FROM user_attempts WHERE session_id = ?", (session_id,)).fetchall()
    
    total = len(attempts)
    correct = sum(1 for a in attempts if a['is_correct'] == 1)
    accuracy = (correct / total) if total > 0 else 0.0
    
    scaled_score = 200 + int(accuracy * 600) if total > 0 else 200
    if session_row['section'] == 'Full Test':
        scaled_score = 400 + int(accuracy * 1200) if total > 0 else 400
        
    cursor.execute("""
        UPDATE practice_sessions 
        SET status = 'completed', score_scaled = ?, completed_at = ?
        WHERE id = ?
    """, (scaled_score, completed_at, session_id))
    
    return {
        "completed": True,
        "total_attempted": total,
        "correct_count": correct,
        "score_scaled": scaled_score
    }

@router.post("/sessions/{session_id}/submit")
async def submit_answer(session_id: str, req: AnswerSubmitRequest):
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Verify question and check if correct
        q_row = cursor.execute("SELECT correct_answer_value, question_type FROM questions WHERE id = ?", (req.question_id,)).fetchone()
        if not q_row:
            raise HTTPException(status_code=404, detail="Question not found")
            
        # Delete existing attempt if any
        cursor.execute("DELETE FROM user_attempts WHERE session_id = ? AND question_id = ?", (session_id, req.question_id))
        
        is_correct = 0
        if q_row['question_type'] == 'Multiple Choice' and req.selected_choice_id:
            c_row = cursor.execute("SELECT is_correct FROM choices WHERE id = ?", (req.selected_choice_id,)).fetchone()
            if c_row and c_row['is_correct']:
                is_correct = 1
        elif q_row['question_type'] == 'Student-Produced Response' and req.student_produced_answer:
            if req.student_produced_answer.strip() == (q_row['correct_answer_value'] or '').strip():
                is_correct = 1

        cursor.execute("""
            INSERT INTO user_attempts (session_id, question_id, selected_choice_id, student_produced_answer, is_correct, time_spent_seconds, bookmarked)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (session_id, req.question_id, req.selected_choice_id, req.student_produced_answer, is_correct, req.time_spent_seconds, 1 if req.bookmarked else 0))

    return {"status": "success", "is_correct": is_correct}

@router.post("/sessions/{session_id}/complete")
async def complete_session_manual(session_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        session_row = cursor.execute("SELECT * FROM practice_sessions WHERE id = ?", (session_id,)).fetchone()
        if not session_row:
            raise HTTPException(status_code=404, detail="Session not found")
        return await complete_session_internal(cursor, session_id, session_row)

@router.get("/sessions")
async def list_sessions():
    with get_db() as conn:
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM practice_sessions ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]

@router.post("/drill")
async def create_drill_session(req: DrillRequest):
    session_id = f"sess_drill_{uuid.uuid4().hex[:10]}"
    time_limit = req.num_questions * 90
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Check if enough questions exist
        count_row = cursor.execute("SELECT count(*) as cnt FROM questions WHERE topic = ? AND subtopic = ?", (req.topic, req.subtopic)).fetchone()
        if count_row['cnt'] == 0:
            raise HTTPException(status_code=404, detail="No questions found for this topic.")
            
        # We will set session_type to 'drill_topic_subtopic' so next_module knows what to do,
        # but our current next_module is hardcoded for 'Reading & Writing'/'Math'/'Full Test'.
        # For simplicity, we can insert it as a 'practice' session but we need a way to serve the questions.
        # Actually, if we just create a session and we need next_module to serve these 10 questions.
        # Let's modify the session_type to include 'drill' so next_module handles it.
        
        cursor.execute("""
            INSERT INTO practice_sessions (id, title, section, session_type, total_questions, time_limit_seconds, status)
            VALUES (?, ?, ?, ?, ?, ?, 'in_progress')
        """, (session_id, f"Drill: {req.subtopic}", req.section, f"drill|{req.topic}|{req.subtopic}", req.num_questions, time_limit))
        
    return {
        "session_id": session_id,
        "title": f"Drill: {req.subtopic}",
        "section": req.section,
        "total_questions": req.num_questions
    }

