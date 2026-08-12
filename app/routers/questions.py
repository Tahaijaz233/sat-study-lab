from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List
from app.database import get_db, is_postgres
from app.agents.ingestion import IngestionAgent
from app.agents.normalization import NormalizationAgent

router = APIRouter(prefix="/api/questions", tags=["Questions"])
ingestion_agent = IngestionAgent()
normalization_agent = NormalizationAgent()


@router.get("")
@router.get("/")
async def list_questions(
    q: Optional[str] = None,
    section: Optional[str] = None,
    difficulty: Optional[str] = None,
    page: int = 1,
    per_page: int = 20
):
    with get_db() as conn:
        cursor = conn.cursor()
        
        offset = (page - 1) * per_page
        where_clauses = ["q.import_status = 'active'"]
        filter_params = []
        
        if section:
            where_clauses.append("q.section = ?")
            filter_params.append(section)
        if difficulty:
            where_clauses.append("q.difficulty = ?")
            filter_params.append(difficulty)
            
        where_sql = " AND ".join(where_clauses)
        
        # Explicitly select only the fields safe to expose to students
        # Exclude answer_explanation and correct_answer_value
        safe_question_cols = """
            q.id, q.passage_id, q.section, q.topic, q.subtopic,
            q.question_type, q.difficulty, q.prompt, q.source_name,
            q.source_uri, q.import_status, q.license_notes, q.content_hash,
            q.created_at
        """
        
        if q:
            # Full-text search - works for both SQLite (FTS5) and PostgreSQL (tsvector)
            if is_postgres():
                # PostgreSQL uses tsvector with @@ operator
                search_sql = """
                    SELECT DISTINCT {safe_question_cols}, p.title as passage_title, p.content as passage_content
                    FROM questions q
                    LEFT JOIN passages p ON q.passage_id = p.id
                    WHERE {where_sql} AND q.search_vector @@ to_tsquery('english', %s)
                    ORDER BY q.created_at DESC
                    LIMIT %s OFFSET %s
                """.format(safe_question_cols=safe_question_cols, where_sql=where_sql)
                exec_params = filter_params + [q, per_page, offset]
                count_sql = f"SELECT COUNT(DISTINCT q.id) FROM questions q LEFT JOIN passages p ON q.passage_id = p.id WHERE {where_sql} AND q.search_vector @@ to_tsquery('english', %s)"
                count_params = filter_params + [q]
            else:
                # SQLite uses FTS5 MATCH
                search_sql = f"""
                    SELECT DISTINCT {safe_question_cols}, p.title as passage_title, p.content as passage_content
                    FROM questions q
                    JOIN questions_fts fts ON q.id = fts.question_id
                    LEFT JOIN passages p ON q.passage_id = p.id
                    WHERE {where_sql} AND questions_fts MATCH ?
                    ORDER BY q.created_at DESC
                    LIMIT ? OFFSET ?
                """
                exec_params = filter_params + [q, per_page, offset]
                count_sql = f"SELECT COUNT(DISTINCT q.id) FROM questions q JOIN questions_fts fts ON q.id = fts.question_id WHERE {where_sql} AND questions_fts MATCH ?"
                count_params = filter_params + [q]
            
        else:
            sql = f"""
                SELECT {safe_question_cols}, p.title as passage_title, p.content as passage_content
                FROM questions q
                LEFT JOIN passages p ON q.passage_id = p.id
                WHERE {where_sql}
                ORDER BY q.created_at DESC
                LIMIT ? OFFSET ?
            """
            exec_params = filter_params + [per_page, offset]
            count_sql = f"SELECT COUNT(*) FROM questions q WHERE {where_sql}"
            count_params = filter_params
        
        if q and is_postgres():
            rows = cursor.execute(search_sql, exec_params).fetchall()
        elif q:
            rows = cursor.execute(search_sql, exec_params).fetchall()
        else:
            rows = cursor.execute(sql, exec_params).fetchall()
        
        questions = []
        for r in rows:
            q_dict = dict(r)
            if is_postgres():
                choices = cursor.execute("SELECT id, choice_letter, content FROM choices WHERE question_id = %s ORDER BY choice_letter", (r['id'],)).fetchall()
            else:
                choices = cursor.execute("SELECT id, choice_letter, content FROM choices WHERE question_id = ? ORDER BY choice_letter", (r['id'],)).fetchall()
            q_dict['choices'] = [{"id": c["id"], "choice_letter": c["choice_letter"], "content": c["content"]} for c in choices]
            questions.append(q_dict)
            
        if is_postgres():
            total_count = cursor.execute(count_sql, count_params).fetchone()[0]
        else:
            total_count = cursor.execute(count_sql, count_params).fetchone()[0]

    return {
        "questions": questions,
        "total": total_count,
        "page": page,
        "per_page": per_page
    }

@router.post("/ingest/opensat")
async def ingest_opensat():
    """Trigger ingestion of OpenSAT public dataset into SQLite."""
    stats = ingestion_agent.from_opensat_api()
    return {"status": "success", **stats}

@router.get("/{question_id}")
async def get_question(question_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        # Explicitly select only the fields safe to expose to students
        # Exclude answer_explanation and correct_answer_value
        if is_postgres():
            row = cursor.execute("""
                SELECT 
                    q.id, q.passage_id, q.section, q.topic, q.subtopic,
                    q.question_type, q.difficulty, q.prompt, q.source_name,
                    q.source_uri, q.import_status, q.license_notes, q.content_hash,
                    q.created_at,
                    p.title as passage_title, p.content as passage_content
                FROM questions q
                LEFT JOIN passages p ON q.passage_id = p.id
                WHERE q.id = %s
            """, (question_id,)).fetchone()
            choices = cursor.execute("SELECT id, choice_letter, content FROM choices WHERE question_id = %s ORDER BY choice_letter", (question_id,)).fetchall()
        else:
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
            """, (question_id,)).fetchone()
            choices = cursor.execute("SELECT id, choice_letter, content FROM choices WHERE question_id = ? ORDER BY choice_letter", (question_id,)).fetchall()
        
        if not row:
            raise HTTPException(status_code=404, detail="Question not found")
            
        q_dict = dict(row)
        q_dict['choices'] = [{"id": c["id"], "choice_letter": c["choice_letter"], "content": c["content"]} for c in choices]
        return q_dict

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    source_info = {"name": file.filename, "type": "pdf_upload"}
    raw_items = ingestion_agent.ingest_pdf(contents, source_info)
    return {"status": "success", "parsed_items_count": len(raw_items)}
